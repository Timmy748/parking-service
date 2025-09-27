"""Model para representar um Cliente do estacionamento."""

from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    """Representa um Cliente do estacionamento.

    Attributes:
        user (OneToOneField): Chave estrangeira para a Model User.
        name (CharField): Nome do Cliente.
        cpf (CharField): CPF do Cliente.
        phone (CharField): Telefone do Cliente.
        created_at (DateTimeField): Metadado de quando foi criado o registro.
        updated_at (DateTimeField): Metadado de quando foi alterado o registro.

    """

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="customer",
        verbose_name="Usuário",
    )

    name = models.CharField(max_length=100, verbose_name="Nome")

    cpf = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="CPF"
    )

    phone = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Telefone"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Criado em"
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self) -> str:
        return self.name
