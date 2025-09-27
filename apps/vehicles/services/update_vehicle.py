"""Service para atualizar o vehicle."""

from django.db import transaction
from django.db.models import Model
from django.utils.text import slugify

from utils.services import update_service

from ..models import (
    Vehicle,
    VehicleBrand,
    VehicleColor,
    VehicleModel,
    VehicleType,
)
from ..schemas import PatchVehicleSchema


@transaction.atomic
def update_vehicle[T: Model](
    payload: PatchVehicleSchema,
    vehicle: Vehicle,
    save: bool = True,
) -> Vehicle:
    """Atualiza um `Vehicle` a partir dos dados fornecidos em `payload`.

    Converte o `payload` em um dicionário com `exclude_unset=True`.
    Para cada campo relacional mapeado para um `Model`, resolve o valor assim:

    - `int` -> busca pela PK;
    - `str` -> normaliza/slugifica e busca ou cria pelo nome;
    - `None` -> deixa como está;

    Depois de resolver os relacionamentos, atualiza os demais atributos usando
    `update_service(data, vehicle)` e, se `save=True`, chama `vehicle.save()`.

    Args:
        payload (PatchVehicleSchema): Dados de atualização.
        vehicle (Vehicle): Instância de `Vehicle` a ser atualizada in-place.
        save (bool, optional): Se `True`, persiste as mudanças com
         `vehicle.save()`. Padrão: `True`.

    Returns:
        Vehicle: A instância `vehicle` modificada.

    """

    def resolve_relationship(
        model: type[T], value: int | str | None
    ) -> T | None:
        if value is None:
            return None

        if isinstance(value, int):
            return model.objects.get(id=value)

        value = slugify(value.strip(" "), allow_unicode=True)
        obj, _ = model.objects.get_or_create(name=value)
        return obj

    data = payload.dict(exclude_unset=True)

    relation_map: dict[str, type[T]] = {
        "vehicle_type": VehicleType,
        "brand": VehicleBrand,
        "color": VehicleColor,
        "model": VehicleModel,
    }

    for field, model in relation_map.items():
        field_value = data.pop(field, None)
        value = resolve_relationship(model, field_value)
        if value:
            setattr(vehicle, field, value)

    update_service(data, vehicle)

    if save:
        vehicle.save()

    return vehicle
