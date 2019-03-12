from collections import namedtuple

from usaspending_api.awards.models import Award, Subaward
from usaspending_api.awards.models import TransactionNormalized
from usaspending_api.awards.serializers import AwardSerializer, SubawardSerializer, TransactionNormalizedSerializer
from usaspending_api.common.mixins import FilterQuerysetMixin, AggregateQuerysetMixin
from usaspending_api.common.serializers import AggregateSerializer
from usaspending_api.common.views import DetailViewSet, CachedDetailViewSet, AutocompleteView

AggregateItem = namedtuple("AggregateItem", ["field", "func"])


class AwardAggregateViewSet(FilterQuerysetMixin, AggregateQuerysetMixin, CachedDetailViewSet):
    """
    Return aggregated award information.
    """

    serializer_class = AggregateSerializer

    def get_queryset(self):
        queryset = Award.objects.all()
        queryset = self.filter_records(self.request, queryset=queryset)
        queryset = self.aggregate(self.request, queryset=queryset)
        queryset = self.order_records(self.request, queryset=queryset)
        return queryset


class AwardListViewSet(FilterQuerysetMixin, CachedDetailViewSet):
    """
    ## Spending data by Award (i.e. a grant, contract, loan, etc)
    This endpoint allows you to search and filter by almost any attribute of an award object.
    """

    filter_map = {"awarding_fpds": "awarding_agency__fpds_code", "funding_fpds": "funding_agency__fpds_code"}
    serializer_class = AwardSerializer

    def get_queryset(self):
        """
        Return the view's queryset.
        """
        queryset = Award.nonempty.all()
        queryset = self.serializer_class.setup_eager_loading(queryset)
        filtered_queryset = self.filter_records(self.request, queryset=queryset, filter_map=self.filter_map)
        ordered_queryset = self.order_records(self.request, queryset=filtered_queryset)
        return ordered_queryset


class AwardRetrieveViewSet(FilterQuerysetMixin, DetailViewSet):
    """
    ## Spending data by Award (i.e. a grant, contract, loan, etc)
    This endpoint allows you to search and filter by almost any attribute of an award object.
    """

    filter_map = {"awarding_fpds": "awarding_agency__fpds_code", "funding_fpds": "funding_agency__fpds_code"}
    serializer_class = AwardSerializer

    def get_queryset(self):
        """
        Return the view's queryset.
        """
        queryset = Award.nonempty.all()
        queryset = self.serializer_class.setup_eager_loading(queryset)
        filtered_queryset = self.filter_records(self.request, queryset=queryset, filter_map=self.filter_map)
        ordered_queryset = self.order_records(self.request, queryset=filtered_queryset)
        return ordered_queryset


class SubawardAggregateViewSet(FilterQuerysetMixin, AggregateQuerysetMixin, CachedDetailViewSet):
    """
    Return aggregated award information.
    """

    serializer_class = AggregateSerializer

    def get_queryset(self):
        queryset = Subaward.objects.all()
        queryset = self.filter_records(self.request, queryset=queryset)
        queryset = self.aggregate(self.request, queryset=queryset)
        queryset = self.order_records(self.request, queryset=queryset)
        return queryset


class SubawardAutocomplete(FilterQuerysetMixin, AutocompleteView):
    """
    Autocomplete support for subaward objects.
    """

    # Maybe refactor this out into a nifty autocomplete abstract class we can just inherit?
    serializer_class = SubawardSerializer

    def get_queryset(self):
        """
        Return the view's queryset.
        """
        queryset = Subaward.objects.all()
        queryset = self.serializer_class.setup_eager_loading(queryset)
        filtered_queryset = self.filter_records(self.request, queryset=queryset)
        ordered_queryset = self.order_records(self.request, queryset=filtered_queryset)
        return ordered_queryset


class SubawardListViewSet(FilterQuerysetMixin, CachedDetailViewSet):
    """
    ## Spending data by Subaward
    This endpoint allows you to search and filter by almost any attribute of a subaward object.
    """

    serializer_class = SubawardSerializer

    def get_queryset(self):
        """
        Return the view's queryset.
        """
        queryset = Subaward.objects.all()
        queryset = self.serializer_class.setup_eager_loading(queryset)
        queryset = self.filter_records(self.request, queryset=queryset)
        queryset = self.order_records(self.request, queryset=queryset)
        return queryset


class SubawardRetrieveViewSet(FilterQuerysetMixin, DetailViewSet):
    """
    ## Spending data by Subaward
    This endpoint allows you to search and filter by almost any attribute of a subaward object.
    """

    serializer_class = SubawardSerializer

    def get_queryset(self):
        """
        Return the view's queryset.
        """
        queryset = Subaward.objects.all()
        queryset = self.serializer_class.setup_eager_loading(queryset)
        queryset = self.filter_records(self.request, queryset=queryset)
        queryset = self.order_records(self.request, queryset=queryset)
        return queryset


class TransactionAggregateViewSet(FilterQuerysetMixin, AggregateQuerysetMixin, CachedDetailViewSet):
    """
    Return aggregated transaction information.
    """

    serializer_class = AggregateSerializer

    def get_queryset(self):
        queryset = TransactionNormalized.objects.all()
        queryset = self.filter_records(self.request, queryset=queryset)
        queryset = self.aggregate(self.request, queryset=queryset)
        queryset = self.order_records(self.request, queryset=queryset)
        return queryset


class TransactionListViewset(FilterQuerysetMixin, CachedDetailViewSet):
    """
    Handles requests for award transaction data.
    """

    serializer_class = TransactionNormalizedSerializer

    def get_queryset(self):
        """
        Return the view's queryset.
        """
        queryset = TransactionNormalized.objects.all()
        queryset = self.serializer_class.setup_eager_loading(queryset)
        filtered_queryset = self.filter_records(self.request, queryset=queryset)
        ordered_queryset = self.order_records(self.request, queryset=filtered_queryset)
        return ordered_queryset


class TransactionRetrieveViewset(FilterQuerysetMixin, DetailViewSet):
    """
    Handles requests for award transaction data.
    """

    serializer_class = TransactionNormalizedSerializer

    def get_queryset(self):
        """
        Return the view's queryset.
        """
        queryset = TransactionNormalized.objects.all()
        queryset = self.serializer_class.setup_eager_loading(queryset)
        filtered_queryset = self.filter_records(self.request, queryset=queryset)
        ordered_queryset = self.order_records(self.request, queryset=filtered_queryset)
        return ordered_queryset
