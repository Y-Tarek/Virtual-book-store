""" This file will hold general filters classes and methods """

from django_filters import rest_framework as filters

class DynamicDateRangeFilter(filters.CharFilter):
    def filter(self, queryset, value):
        if value:
            day_range = value.split(",")
            field_name = self.field_name.split("_day_range")[0]
            lookup_expr = f"{field_name}__date__range"
            return queryset.filter(**{lookup_expr: day_range})
        return queryset

class PublishedDateRangeFilter(filters.FilterSet):
    """This class will hold a general date range filter"""

    published_date_day_range = DynamicDateRangeFilter(field_name="published_date_day_range")