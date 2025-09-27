"""Signal para atualizar o status da vaga de estacionamento."""

from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import ParkingRecord, ParkingSpot


@receiver(post_save, sender=ParkingRecord)
def update_parking_spot_status(
    sender: type[ParkingRecord],
    instance: ParkingRecord,
    created: bool,
    **kwargs: Any,
) -> None:
    """Atualiza o status da vaga de estacionamento com base no registro.

    Args:
        sender (type[ParkingRecord]): Modelo que enviou o sinal.
        instance (ParkingRecord): Instância do registro de estacionamento.
        created (bool): Indica se a instância foi criada.
        **kwargs (Any): Argumentos adicionais.

    """
    parking_spot: ParkingSpot = instance.parking_spot
    parking_spot.is_occupied = instance.exit_time is None
    print(parking_spot.is_occupied)
    parking_spot.save()
