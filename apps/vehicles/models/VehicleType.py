"""Model para representar um Tipo de Veículo."""

from django.db import models


class VehicleType(models.Model):
    """Representa um Tipo de Veículo.

    Attributes:
        name (CharField): Nome do Tipo do Veículo.
        description (TextField): Descrição do Tipo do Veículo.
        created_at (DateTimeField): Metadado de quando foi criado o registro.
        updated_at (DateTimeField): Metadado de quando foi alterado o registro.

    """

    name = models.CharField(max_length=50, unique=True, verbose_name="Nome")

    description = models.TextField(
        blank=True, null=True, verbose_name="Descrição"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Criado em"
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Tipo de Veículo"
        verbose_name_plural = "Tipos de Veículos"

    def __str__(self) -> str:
        return self.name
