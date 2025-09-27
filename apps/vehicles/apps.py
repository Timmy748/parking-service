from django.apps import AppConfig


class VehiclesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.vehicles"
    verbose_name = "Veículos"

    def ready(self) -> None:
        import apps.vehicles.signals
