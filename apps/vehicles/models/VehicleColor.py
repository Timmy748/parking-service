"""Modelo para representar uma Cor de veículo."""

from django.db import models


class VehicleColor(models.Model):
    """Representa uma Cor de veículo.

    Attributes:
        name (CharField): Nome da Cor de veículo.
        hex_code (CharField): Codígo Hexadecimal.
        created_at (DateTimeField): Metadado de quando foi criado o registro.
        updated_at (DateTimeField): Metadado de quando foi alterado o registro.

    """

    name = models.CharField(max_length=50, unique=True, verbose_name="Nome")

    hex_code = models.CharField(
        max_length=6,
        unique=True,
        verbose_name="Codígo Hexadecimal",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Criado em"
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Cor de Veículo"
        verbose_name_plural = "Cores de Veículos"

    def __str__(self) -> str:
        return f"{self.name} - #{self.hex_code}"
