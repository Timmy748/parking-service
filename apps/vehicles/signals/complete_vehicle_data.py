""""Signals para completar os dados do veículo."""

from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Vehicle
from ..tasks import complete_vehicle_data


@receiver(post_save, sender=Vehicle)
def complete_vehicle_data_post_save(
    sender: type[Vehicle], instance: Vehicle, created: bool, **kwargs: Any
) -> None:
    """Signal para completar os dados do veículo após a criação.

    Args:
        sender (type[Vehicle]): Model de Vehicle.
        instance (Vehicle): Instância de Vehicle.
        created (bool): Criado ou não.
        kwargs (Any): Parâmetros nomeados adicionais.

    """
    missing_fields: bool = (
        not instance.brand or
        not instance.color or
        not instance.model
    )

    if created and missing_fields:
        complete_vehicle_data.delay(instance.license_plate)

