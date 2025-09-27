"""Model para o registro de estacionamento de veículos."""

from django.contrib.auth.models import User
from django.db import models

from apps.vehicles.models.Vehicle import Vehicle
from utils.services import is_internal_user

from .ParkingSpot import ParkingSpot


class OwnerQueryset(models.QuerySet["ParkingRecord"]):
    """QuerySet personalizado para o modelo ParkingRecord.

    Adiciona o método for_owner para filtrar registros pelo dono do veículo.

    """

    def for_owner(self, user: User) -> models.QuerySet["ParkingRecord"]:
        """Retorna um QuerySet de ParkingRecord filtrando pelo usuário dono.

        Se o `user` for um admin ou super_user (verificado pela função
        is_internal_user), retorna todas as instâncias.
        Caso contrário, retorna apenas os registros cujos veículos pertencem
        ao usuário.

        Args:
            user (User): Instância do usuário a ser verificada.

        Returns:
            QuerySet[ParkingRecord]: Queryset com todas as instancias de
            ParkingRecords se for um admin ou super_user ou apenas a
            que é dono do veículo.

        """
        if is_internal_user(user):
            return self.all()
        return self.filter(vehicle__owner=user)


class OwnerManager(models.Manager):
    """Manager personalizado para o modelo ParkingRecord.

    Adiciona o método for_owner para filtrar registros pelo dono do veículo.

    """

    def get_queryset(self) -> OwnerQueryset:
        """Retorna o QuerySet padrão do OwnerManager.

        Returns:
            OwnerQueryset: QuerySet tipado do modelo associado.

        """
        return OwnerQueryset(self.model, using=self._db)

    def for_owner(self, user: User) -> models.QuerySet["ParkingRecord"]:
        """Retorna um QuerySet de ParkingRecord filtrando pelo usuário dono.

        Args:
            user (User): Instância do usuário a ser verificada.

        Returns:
            QuerySet[ParkingRecord]: Queryset com todas as instancias de
            ParkingRecords se for um admin ou super_user ou apenas a
            que é dono do veículo.

        """
        return self.get_queryset().for_owner(user)


class ParkingRecord(models.Model):
    """Model para o registro de estacionamento de veículos.

    Attributes:
        vehicle (ForeignKey): Chave estrangeira para a Model Vehicle.
        parking_spot (ForeignKey): Chave estrangeira para a Model ParkingSpot.
        entry_time (DateTimeField): Horário de entrada na vaga.
        exit_time (DateTimeField): Horário de saída da vaga.
        objects (OwnerManager): Manager personalizado com o método for_owner.

    """

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name="parking_records",
        verbose_name="Veículo",
    )

    parking_spot = models.ForeignKey(
        ParkingSpot,
        on_delete=models.PROTECT,
        related_name="parking_records",
        verbose_name="Vaga",
    )

    entry_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Horário de Entrada"
    )

    exit_time = models.DateTimeField(
        blank=True, null=True, verbose_name="Horário de Saída"
    )

    objects: OwnerManager = OwnerManager()

    class Meta:
        verbose_name = "Registro"
        verbose_name_plural = "Registros"

    def __str__(self) -> str:
        return f"{self.vehicle} - {self.parking_spot} - {self.entry_time}"
