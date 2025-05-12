"""
Enum for user roles in the application.
"""
from django.utils.translation import gettext_lazy as _


class Roles:
    """Editor role can create and edit of books."""
    EDITOR = "editor"
    """Reader role can only read books."""
    READER = "reader"

    CHOICES = [
        (EDITOR, _("Editor")),
        (READER, _("Reader")),
    ]
