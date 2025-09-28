"""Modelo para representar um veículo registrado no estacionamento."""

from django.contrib.auth.models import User
from django.db import models

from utils.services import is_internal_user

from .VehicleBrand import VehicleBrand
from .VehicleColor import VehicleColor
from .VehicleModel import VehicleModel
from .VehicleType import VehicleType


class OwnerQueryset(models.QuerySet["Vehicle"]):
    """QuerySet personalizado para o modelo Vehicle.

    Adiciona o método for_owner para filtrar registros pelo dono do veículo.

    """

    def for_owner(self, user: User) -> models.QuerySet["Vehicle"]:
        """Retorna um QuerySet de Vehicle filtrando pelo usuário dono.

        Se o `user` for um admin ou super_user (verificado pela função
        is_internal_user), retorna todas as instâncias.
        Caso contrário, retorna apenas os registros cujos veículos pertencem
        ao usuário.

        Args:
            user (User): Instância do usuário a ser verificada.

        Returns:
            QuerySet[Vehicle]: Queryset com todas as instancias de Vehicles
            se for um admin ou super_user ou apenas a que é dono do veículo.

        """
        if is_internal_user(user):
            return self.select_related()
        return self.select_related().filter(owner=user)


class OwnerManager(models.Manager):
    """Manager personalizado para o modelo Vehicle.

    Adiciona o método for_owner para filtrar registros pelo dono do veículo.

    """

    def get_queryset(self) -> OwnerQueryset:
        """Retorna o QuerySet padrão do OwnerManager.

        Returns:
            OwnerQueryset: QuerySet tipado do modelo associado.

        """
        return OwnerQueryset(self.model, using=self._db)

    def for_owner(self, user: User) -> models.QuerySet["Vehicle"]:
        """Retorna um QuerySet de Vehicle filtrando pelo usuário dono.

        Args:
            user (User): Instância do usuário a ser verificada.

        Returns:
            QuerySet[Vehicle]: Queryset com todas as instancias de Vehicles
            se for um admin ou super_user ou apenas a que é dono do veículo.

        """
        return self.get_queryset().for_owner(user)


class Vehicle(models.Model):
    """Representa um Veículo registrado no estacionamento.

    Attributes:
        vehicle_type (ForeignKey): Chave estrangeira para a Model VehicleType.
        owner (OneToOneField): Chave estrangeira para a Model User.
        license_plate (CharField): Placa do Veículo.
        brand (ForeignKey): Chave estrangeira para a Marca do Veículo.
        model (ForeignKey): Chave estrangeira para o Modelo do Veículo.
        color (ForeignKey): Chave estrangeira para a Cor do Veículo.
        created_at (DateTimeField): Metadado de quando foi criado o Registro.
        updated_at (DateTimeField): Metadado de quando foi alterado o Registro.
        objects (OwnerManager): Manager personalizado com o método for_owner.

    """

    vehicle_type = models.ForeignKey(
        VehicleType,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="vehicles",
        verbose_name="Tipo do Veículo",
    )

    owner = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="vehicles",
        verbose_name="proprietário",
    )

    license_plate = models.CharField(
        max_length=10, unique=True, verbose_name="Placa"
    )

    brand = models.ForeignKey(
        VehicleBrand,
        blank=True,
        null=True,
        verbose_name="Marca",
        on_delete=models.PROTECT,
    )

    model = models.ForeignKey(
        VehicleModel,
        blank=True,
        null=True,
        verbose_name="Modelo",
        on_delete=models.PROTECT,
    )

    color = models.ForeignKey(
        VehicleColor,
        blank=True,
        null=True,
        verbose_name="Cor",
        on_delete=models.PROTECT,
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Criado em"
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Atualizado em"
    )

    objects: OwnerManager = OwnerManager()

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"

    def __str__(self) -> str:
        return self.license_plate
