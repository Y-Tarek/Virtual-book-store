""" This file will hold app apis filter classes """
from django_filters import rest_framework as filters
from shared.filters import (
    PublishedDateRangeFilter
)

class BookFilter(PublishedDateRangeFilter):
    """ This class will hold book list filters """

    author = filters.CharFilter(
        field_name="author__username",
        lookup_expr="iexact"
    )