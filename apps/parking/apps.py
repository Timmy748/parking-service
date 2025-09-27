from django.apps import AppConfig


class ParkingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.parking"
    verbose_name = "Estacionamento"

    def ready(self) -> None:
        import apps.parking.signals
