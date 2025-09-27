"""Model para representar uma Marca de Veículo."""

from django.db import models


class VehicleBrand(models.Model):
    """Representa uma Marca de Veículo.

    Attributes:
        name (CharField): Nome da Marca do Veículo.
        created_at (DateTimeField): Metadado de quando foi criado o registro.
        updated_at (DateTimeField): Metadado de quando foi alterado o registro.

    """

    name = models.CharField(max_length=50, unique=True, verbose_name="Nome")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Criado em"
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Marca de Veículo"
        verbose_name_plural = "Marcas de Veículos"

    def __str__(self) -> str:
        return self.name
