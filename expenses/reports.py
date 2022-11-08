from collections import OrderedDict

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


def total_amount_spent(queryset):
    result = [
        x for x in OrderedDict(queryset.aggregate(Sum('amount'))).values()
    ]
    return result[0]

def summary_per_months(queryset):
    result_dict = {}

    result = OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('date', Value('-')))
        .order_by()
        .values('date')
        .annotate(s=Sum('amount'))
        .values_list('date', 's')
    ))
    comp_result = [x for x in result.items()]

    for item in comp_result:
        replaced_date = item[0].replace(day=1)
        if replaced_date in result_dict:
            result_dict[replaced_date] += item[1]
        else:
            result_dict[replaced_date] = item[1]

    return OrderedDict(result_dict)
