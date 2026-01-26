from django.apps import AppConfig


class LandmarkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landmark'
    def ready(self):
        import landmark.signals  # Import the signals module to register the signal
