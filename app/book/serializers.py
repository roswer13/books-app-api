"""
Serializer for Book model and Page model.
"""
from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from core.models import Book, Page


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.
    """
    class Meta:
        model = Book
        fields = ['uuid', 'title', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'uuid', 'created_at', 'updated_at',]


class PageSerializer(serializers.ModelSerializer):
    """
    Serializer for Page model.
    """
    book = serializers.SlugRelatedField(
        queryset=Book.objects.all(),
        slug_field='uuid',
    )

    class Meta:
        model = Page
        fields = ['uuid', 'book', 'number', 'content',]
        read_only_fields = ['id', 'uuid',]


class PageDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Page model with book details.
    """

    class Meta:
        model = Page
        fields = ['uuid', 'number', 'content',]
        read_only_fields = ['id', 'uuid',]

    def validate(self, attrs):
        book = attrs.get(
            'book', self.instance.book if self.instance else None
        )
        number = attrs.get(
            'number', self.instance.number if self.instance else None
        )

        if Page.objects.filter(book=book, number=number).exclude(
            pk=self.instance.pk if self.instance else None
        ).exists():
            raise serializers.ValidationError(
                {"number": _("A page with this number already exists.")}
            )
        return attrs
