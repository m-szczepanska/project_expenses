from django.db.models import Q
from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 10


    def get_ordering(self):
        ordering = self.request.GET.get('order_by')
        return ordering

    def get_context_data(self, *, object_list=None, **kwargs):

        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            category = form.cleaned_data.get('category', '')
            date = form.cleaned_data.get('date', '')
            date_from = form.data.get('date_from', '')
            date_to = form.data.get('date_to', '')

            if category:
                queryset = queryset.filter(category__name__icontains=category)
            if date:
                queryset = queryset.filter(date__icontains=date)
            if date_from and date_to:
                queryset = queryset.filter(date__gte=date_from, date__lte=date_to)
            elif date_from:
                queryset = queryset.filter(date__gte=date_from, date__lte=date_to)

            ordering = self.get_ordering()
            if ordering:
                queryset = queryset.order_by(ordering)

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5