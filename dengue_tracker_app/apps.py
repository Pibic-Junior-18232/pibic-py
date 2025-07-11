from django.apps import AppConfig


class DengueTrackerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dengue_tracker_app'

    def ready(self):
        import dengue_tracker_app.signals
