from django.apps import AppConfig


class DateExtractionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.date_extraction'
    def ready(self):
        from date_extraction.logic import main
        return main.main()