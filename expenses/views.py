from django.db.models import Q
from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            category = form.cleaned_data.get('category', '')
            name = form.cleaned_data.get('name', '').strip()
            amount = form.cleaned_data.get('amount', '')
            date = form.cleaned_data.get('date', '')

            if category:
                queryset = queryset.filter(category__name__icontains=category)
            if name:
                queryset = queryset.filter(name__icontains=name)
            if amount:
                queryset = queryset.filter(amount__icontains=amount)
            if date:
                queryset = queryset.filter(date__icontains=date)

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            **kwargs)

class CategoryListView(ListView):
    model = Category
    paginate_by = 5

