from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Вьюсет, позволяющий осуществлять GET, POST и DELETE запросы."""
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    lookup_field = 'slug'
