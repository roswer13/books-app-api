"""
Book model
"""
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    """Book in the system."""
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, help_text=_('Unique identifier for the book.')
    )
    title = models.CharField(
        verbose_name=_('Title'), max_length=128,
        help_text=_('Title of the book.')
    )
    author = models.CharField(
        verbose_name=_('Author'), max_length=128,
        help_text=_('Author of the book.')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Creation date")
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Modification date")
    )

    def __str__(self):
        """Return string representation of book."""
        return self.title


class Page(models.Model):
    """Page in the book."""
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False,
        unique=True, help_text=_('Unique identifier for the page.')
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE,
        related_name='pages', verbose_name=_('Book'),
        help_text=_('Book to which the page belongs.')
    )
    number = models.PositiveIntegerField(
        verbose_name=_('Page number'),
        help_text=_('Number of the page.')
    )
    content = models.TextField(
        verbose_name=_('Content'),
        max_length=2048,
        help_text=_('Content of the page.')
    )

    def __str__(self):
        """Return string representation of page."""
        return f"Page {self.number} of {self.book.title}"
