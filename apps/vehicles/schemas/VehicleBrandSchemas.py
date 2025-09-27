"""Schemas para a model VehicleBrand."""

from datetime import datetime
from typing import Optional

from ninja import Field, FilterSchema, ModelSchema

from ..models import VehicleBrand


class CreateVehicleBrandSchema(ModelSchema):
    """Schema de criação para o VehicleBrand.

    Inclui o campo `name`.

    """

    class Meta:
        model = VehicleBrand
        fields = ["name"]


class VehicleBrandSchema(ModelSchema):
    """Schema de resposta para o VehicleBrand.

    Inclui os campos `id`, `name`, `created_at` e `updated_at`.

    """

    class Meta:
        model = VehicleBrand
        fields = ["id", "name", "created_at", "updated_at"]


class PatchVehicleBrandSchema(ModelSchema):
    """Schema de atualização parcial para o VehicleBrand.

    Permite atualizar o campo `name`. Todos os
    campos são opcionais.

    """

    class Meta:
        model = VehicleBrand
        fields = ["name"]
        fields_optional = ["name"]


class FilterVehicleBrandSchema(FilterSchema):
    """Schema de filtro para consultas na model VehicleBrand.

    Permite filtrar por `name`, `created_at` e `updated_at`.
    O campo `name` suporta buscas parciais
    (case-insensitive).

    """

    name: Optional[str] = Field(None, q=["name__icontains"])
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
