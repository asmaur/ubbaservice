from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1#00
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CustomPagination(LimitOffsetPagination):
    default_limit = 2
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 50

# class CustomPagedResponse(paginated_response.PaginatedResponse):
#     def get_paginated_response(self,):
#         return super()._get_paginated_response()
