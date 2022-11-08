import datetime
from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import (summary_per_category, summary_per_months,
    total_amount_spent)


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 10

    def get_ordering(self):
        ordering = self.request.GET.get('order_by')
        return ordering

    def get_context_data(self, *, object_list=None, **kwargs):

        queryset = object_list if object_list is not None else self.object_list

        if self.request.GET:
            form = ExpenseSearchForm(self.request.GET)

            if form.is_valid():
                categories = form.cleaned_data.get('category', '')
                date_from = form.data.get('date_from', '')
                date_to = form.data.get('date_to', '')

                if categories:
                    queryset = queryset.filter(category__in=categories)
                if date_from and date_to:
                    queryset = queryset.filter(
                        date__gte=date_from, date__lte=date_to
                    )
                elif date_from:
                    date_to = datetime.date.today()
                    queryset = queryset.filter(
                        date__gte=date_from, date__lte=date_to
                    )
                elif date_to:
                    date_from = datetime.date(1900, 1, 1)
                    queryset = queryset.filter(
                        date__gte=date_from, date__lte=date_to
                    )

                ordering = self.get_ordering()
                if ordering:
                    queryset = queryset.order_by(ordering)
        else:
            form = ExpenseSearchForm()

        return super().get_context_data(
            form=form,
            object_list=queryset,
            total_amount_spent=total_amount_spent(queryset),
            summary_per_category=summary_per_category(queryset),
            summary_per_months=summary_per_months(queryset),
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5