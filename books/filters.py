from django_filters.rest_framework import (
    FilterSet, BaseInFilter, NumberFilter, CharFilter
)
from .models import Book


class CharInFilter(BaseInFilter, CharFilter):
    pass


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class BookFilter(FilterSet):
    publisher_id = NumberInFilter(field_name='publisher_id', lookup_expr='in')
    title = CharInFilter(field_name='title', lookup_expr='in')

    class Meta:
        model = Book
        fields = ['title', 'genre', 'publisher_id']
