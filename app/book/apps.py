from django.apps import AppConfig


class BookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'book'

    def ready(self):
        """
        Import signals when the app is ready.
        This ensures that the signals are registered and ready to use.
        """
        import book.signals # noqa
