"""Schemas para a model VehicleModel."""

from datetime import datetime
from typing import Optional

from ninja import Field, FilterSchema, ModelSchema

from ..models import VehicleModel


class CreateVehicleModelSchema(ModelSchema):
    """Schema de criação para o VehicleModel.

    Inclui o campo `name`.

    """

    class Meta:
        model = VehicleModel
        fields = ["name"]


class VehicleModelSchema(ModelSchema):
    """Schema de resposta para o VehicleModel.

    Inclui os campos `id`, `name`, `created_at` e `updated_at`.

    """

    class Meta:
        model = VehicleModel
        fields = ["id", "name", "created_at", "updated_at"]


class PatchVehicleModelSchema(ModelSchema):
    """Schema de atualização parcial para o VehicleModel.

    Permite atualizar o campo `name`. Todos os
    campos são opcionais.

    """

    class Meta:
        model = VehicleModel
        fields = ["name"]
        fields_optional = ["name"]


class FilterVehicleModelSchema(FilterSchema):
    """Schema de filtro para consultas na model VehicleModel.

    Permite filtrar por `name`, `created_at` e `updated_at`.
    O campo `name` suporta buscas parciais
    (case-insensitive).

    """

    name: Optional[str] = Field(None, q=["name__icontains"])
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
