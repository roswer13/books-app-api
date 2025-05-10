"""
Signals for the Book app.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now

from core.models import Page


@receiver([post_save, post_delete], sender=Page)
def update_book_timestamp(sender, instance, **kwargs):
    """
    Update the Book's updated_at timestamp when a Page is saved or deleted.
    """
    book = instance.book
    book.updated_at = now()
    book.save(update_fields=["updated_at"])
