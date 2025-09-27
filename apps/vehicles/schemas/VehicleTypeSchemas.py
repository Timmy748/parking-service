"""Schemas para a model VehicleType."""

from datetime import datetime
from typing import Optional

from ninja import Field, FilterSchema, ModelSchema

from ..models import VehicleType

VEHICLE_TYPE_FIELDS = ["name", "description"]


class CreateVehicleTypeSchema(ModelSchema):
    """Schema de criação para o VehicleType.

    Inclui os campos `name` e `description`.

    """

    class Meta:
        model = VehicleType
        fields = VEHICLE_TYPE_FIELDS


class VehicleTypeSchema(ModelSchema):
    """Schema de resposta para o VehicleType.

    Inclui os campos `id`, `name`, `description`, `created_at` e `updated_at`.

    """

    class Meta:
        model = VehicleType
        fields = ["id", *VEHICLE_TYPE_FIELDS, "created_at", "updated_at"]


class PatchVehicleTypeSchema(ModelSchema):
    """Schema de atualização parcial para o VehicleType.

    Permite atualizar qualquer um dos campos `name` ou `description`. Todos os
    campos são opcionais.

    """

    class Meta:
        model = VehicleType
        fields = VEHICLE_TYPE_FIELDS
        fields_optional = VEHICLE_TYPE_FIELDS


class FilterVehicleTypeSchema(FilterSchema):
    """Schema de filtro para consultas na model VehicleType.

    Permite filtrar por `name`, `description`, `created_at` e `updated_at`.
    Os campos `name` e `description` suportam buscas parciais
    (case-insensitive).

    """

    name: Optional[str] = Field(None, q=["name__icontains"])
    description: Optional[str] = Field(None, q=["description__icontains"])
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
