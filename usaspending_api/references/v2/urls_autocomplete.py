from django.conf.urls import url
from usaspending_api.references.v2.views.autocomplete import AwardingAgencyAutocompleteViewSet
from usaspending_api.references.v2.views.autocomplete import CFDAAutocompleteViewSet
from usaspending_api.references.v2.views.city import CityAutocompleteViewSet
from usaspending_api.references.v2.views.autocomplete import FundingAgencyAutocompleteViewSet
from usaspending_api.references.v2.views.autocomplete import GlossaryAutocompleteViewSet
from usaspending_api.references.v2.views.autocomplete import NAICSAutocompleteViewSet
from usaspending_api.references.v2.views.autocomplete import PSCAutocompleteViewSet
from usaspending_api.references.v2.views.autocomplete import RecipientAutocompleteViewSet

urlpatterns = [
    url(r"^awarding_agency", AwardingAgencyAutocompleteViewSet.as_view()),
    url(r"^funding_agency", FundingAgencyAutocompleteViewSet.as_view()),
    url(r"^cfda", CFDAAutocompleteViewSet.as_view()),
    url(r"^naics", NAICSAutocompleteViewSet.as_view()),
    url(r"^psc", PSCAutocompleteViewSet.as_view()),
    url(r"^recipient", RecipientAutocompleteViewSet.as_view()),
    url(r"^glossary", GlossaryAutocompleteViewSet.as_view()),
    url(r"^city", CityAutocompleteViewSet.as_view()),
]
