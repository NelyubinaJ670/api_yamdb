from rest_framework.pagination import PageNumberPagination

COUNT_USER_PAGINATION = 1


class UserPagination(PageNumberPagination):
    page_size = COUNT_USER_PAGINATION
