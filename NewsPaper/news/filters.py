from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import *


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name="postcategory__category_category",
        queryset=Category.objects.all(),
        label="Категория",
        empty_label="Любая категория"
    )

    date_created_after = DateTimeFilter(
        field_name="date_created",
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'}
        )
    )

    class Meta:
        model = Post
        fields = {
            'title': ["icontains"],
        }

