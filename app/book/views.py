"""
Views for the book APIs.
"""
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

from core.models import Book, Page

from book import serializers, permisions


class BookPagination(PageNumberPagination):
    page_size = 10


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model.
    """
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all().order_by('-created_at')
    pagination_class = BookPagination
    permission_classes = [permisions.IsEditorOrReadOnly]
    lookup_field = 'uuid'


class PagePagination(PageNumberPagination):
    page_size = 15
    invalid_page_message = _('Invalid page number.')
    invalid_page_message_detail = _('Please provide a valid page number.')


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='book_uuid',
            description=_('UUID of the book to filter pages by.'),
            required=True,
            type=str,
            location=OpenApiParameter.QUERY
        )
    ]
)
class PageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Page model.
    """
    serializer_class = serializers.PageDetailSerializer
    queryset = Page.objects.all()
    pagination_class = PagePagination
    permission_classes = [permisions.IsEditorOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['book__uuid']
    lookup_field = 'uuid'

    def get_serializer_class(self):
        """
        Return the serializer class based on the action.
        """
        if self.action in ['list', 'create']:
            return serializers.PageSerializer

        return self.serializer_class

    def get_queryset(self):
        """
        Return the queryset for the Page model.
        """
        queryset = self.queryset

        if self.action == "list":
            book_uuid = self.request.query_params.get("book_uuid")
            if not book_uuid:
                raise ValidationError(
                    {"book_uuid": _("This field is required.")}
                )
            queryset = queryset.filter(book__uuid=book_uuid)

        return queryset.order_by("number")
