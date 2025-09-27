"""Schemas para a model VehicleColor."""

from datetime import datetime
from typing import Optional

from ninja import Field, FilterSchema, ModelSchema

from ..models import VehicleColor

VEHICLE_COLOR_FIELDS = ["name", "hex_code"]


class CreateVehicleColorSchema(ModelSchema):
    """Schema de criação para o VehicleColor.

    Inclui os campos `name` e `hex_code`.

    """

    class Meta:
        model = VehicleColor
        fields = VEHICLE_COLOR_FIELDS


class VehicleColorSchema(ModelSchema):
    """Schema de resposta para o VehicleColor.

    Inclui os campos `id`, `name`, `hex_code`, `created_at` e `updated_at`.

    """

    class Meta:
        model = VehicleColor
        fields = ["id", *VEHICLE_COLOR_FIELDS, "created_at", "updated_at"]


class PatchVehicleColorSchema(ModelSchema):
    """Schema de atualização parcial para o VehicleColor.

    Permite atualizar qualquer um dos campos `name` ou `hex_code`. Todos os
    campos são opcionais.

    """

    class Meta:
        model = VehicleColor
        fields = VEHICLE_COLOR_FIELDS
        fields_optional = VEHICLE_COLOR_FIELDS


class FilterVehicleColorSchema(FilterSchema):
    """Schema de filtro para consultas na model VehicleColor.

    Permite filtrar por `name`, `hex_code`, `created_at` e `updated_at`.
    Os campos `name` e `hex_code` suportam buscas parciais
    (case-insensitive).

    """

    name: Optional[str] = Field(None, q=["name__icontains"])
    hex_code: Optional[str] = Field(None, q=["hex_code__icontains"])
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
