from rest_framework.filters import OrderingFilter


class BasicOrdringFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super(BasicOrdringFilter, self).__init__(*args, **kwargs)

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            return queryset.order_by(*ordering)
        return queryset