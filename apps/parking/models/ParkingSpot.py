"""Model para a Vaga do estacionamento."""

from django.db import models


class ParkingSpot(models.Model):
    """Representa uma Vaga do estacionamento.

    Attributes:
        spot_number (CharField): número da Vaga.
        is_occupied (BooleanField): Se está ou não ocupada.
        created_at (DateTimeField): Metadado de quando foi criado o registro.
        updated_at (DateTimeField): Metadado de quando foi alterado o registro.

    """

    spot_number = models.CharField(
        max_length=10, unique=True, verbose_name="Número da Vaga"
    )

    is_occupied = models.BooleanField(default=False, verbose_name="Ocupado")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Criado em"
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas"

    def __str__(self) -> str:
        return self.spot_number
