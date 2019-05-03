import logging

from django.conf import settings
from rest_framework.response import Response
from time import perf_counter
from collections import OrderedDict

from usaspending_api.common.cache_decorator import cache_response
from usaspending_api.common.views import APIDocumentationView

from usaspending_api.common.elasticsearch.client import es_client_query
from usaspending_api.search.v2.elasticsearch_helper import preprocess


logger = logging.getLogger("console")

TRANSACTIONS_INDEX_ROOT = "{}*".format(settings.TRANSACTIONS_INDEX_ROOT)


class CityAutocompleteViewSet(APIDocumentationView):
    """
    endpoint_doc:
    """

    @cache_response()
    def get(self, request, format=None):
        search_text = request.GET.get("search_text")
        limit = request.GET.get("limit", 10)
        method = request.GET.get("method", "wildcard")


        # query = {
        # "dis_max": {
        #     "queries": [{"query_string": {"query": keyword}}, {"query_string": {"query": keyword, "fields": fields}}]

        search_text = preprocess(search_text)
        if method == "wildcard":
            # query = {
            #     "_source": ["recipient_location_city_name", "recipient_location_state_code", "pop_city_name", "pop_state_code"],
            #     "size": limit,
            #     "query": {
            #         "dis_max": {
            #             "queries": [
            #                 {"query_string": {"wildcard": {"recipient_location_city_name": {"value": search_text + "*"}}}},
            #                 {"query_string": {"wildcard": {"pop_city_name": {"value": search_text + "*"}}}},
            #             ]
            #         }
            #     }
            # }
            query = {
                "_source": ["recipient_location_city_name", "pop_city_name"],
                "size": limit,
                "query": {"query_string": {
                  "query":"{}*".format(search_text),
                  "fields":["recipient_location_city_name", "pop_city_name"]
                  }
                },
                "highlight": {
                    "fields": {
                        "recipient_location_city_name":{},
                        "pop_city_name":{}
                    }
                }
            }
        elif method == "fuzzy":
            query = {
                "_source": ["recipient_location_city_name", "pop_city_name", "award_id"],
                "size": limit,
                "query": {
                  "query_string": {
                    "query":"{}~".format(search_text),
                    "fields":["recipient_location_city_name", "pop_city_name"],
                    "fuzzy_prefix_length" : 1
                  }
                },
                "highlight": {
                    "fields": {
                        "recipient_location_city_name":{},
                        "pop_city_name":{}
                    }
                }
            }

        # https://www.elastic.co/guide/en/elasticsearch/reference/6.1/search-suggesters-completion.html
        # query = {
        #     "suggest": {
        #         "song-suggest" : {
        #             "prefix" : search_text,
        #             "completion" : {
        #                 "field" : "recipient_location_city_name"
        #             }
        #         }
        #     }
        # }

        # Search both fields for exact matches
        # POST city/_search
        # {
        #   "query": {
        #     "multi_match": {
        #       "query": "herndon",
        #       "fields": [
        #         "pop_city_name",
        #         "recipient_location_city_name"
        #       ]
        #     }
        #   }
        # }

        response = OrderedDict(
            [("params", request.GET), ("query", query), ("search-time", 0), ("total-hits", 0), ("terms", [])]
        )

        start_time = perf_counter()

        hits = es_client_query(index="city-search-v1", body=query, retries=10)
        if hits:
            response["total-hits"] = hits["hits"]["total"]
            results = hits["hits"]["hits"]
            terms = []
            for result in results:
                for matched_field, _ in result['highlight'].items():
                    terms.append(result["_source"][matched_field])
            terms = set(terms)
            response['terms'] = terms
        response["search-time"] = perf_counter() - start_time
        return Response(response)
