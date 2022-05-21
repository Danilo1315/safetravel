from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class PlanePagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'p'
    page_size_query_param = 'size'
    last_page_strings = 'end'
    max_page_size = 10
    
    
class PlaneLOPagination(LimitOffsetPagination):
    default_limit = 10