from rest_framework.pagination import CursorPagination

class ProfilePagination(CursorPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    ordering = '-dateCreated'