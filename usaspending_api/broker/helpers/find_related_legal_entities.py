from django.db.models import Count, F
from usaspending_api.awards.models import TransactionNormalized
from usaspending_api.awards.models import Subaward


def find_related_legal_entities(transactions):
    related_le_ids = transactions.values_list('recipient_id', flat=True)
    tn_count = (
        TransactionNormalized.objects.filter(recipient_id__in=related_le_ids)
        .values('recipient_id')
        .annotate(transaction_count=Count('id'))
        .values_list('recipient_id', 'transaction_count')
    )
    tn_count_filtered = (
        transactions.values('recipient_id')
        .annotate(transaction_count=Count('id'))
        .values_list('recipient_id', 'transaction_count')
    )
    recipients_in_subaward = (
        Subaward.objects.filter(prime_recipient__in=related_le_ids)
        .annotate(recipient_id=F("prime_recipient_id"))
        .values_list("recipient_id", flat=True)
    )

    tn_count_mapping = dict(tn_count)
    tn_count_filtered_mapping = dict(tn_count_filtered)
    # only delete legal entities if and only if all their transactions are deleted
    delete_les = set(dict(tn_count_mapping.items() & tn_count_filtered_mapping.items()))
    print("---------------------------------------------------")
    print(delete_les)
    print("Deleting the subaward ones")
    delete_les -= set(recipients_in_subaward)
    print(delete_les)
    return list(delete_les)
