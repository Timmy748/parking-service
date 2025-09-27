"""Schemas para a model ParkingSpot."""

from typing import Optional

from ninja import Field, FilterSchema, ModelSchema

from ..models import ParkingSpot

SPOT_FIELDS = [
    "spot_number",
    "is_occupied",
]


class CreateSpotSchema(ModelSchema):
    """Schema de criação para o ParkingSpot.

    Inclui o campo `spot_number`.

    """

    class Meta:
        model = ParkingSpot
        fields = [
            "spot_number",
        ]


class SpotSchema(ModelSchema):
    """Schema de resposta para o ParkingSpot.

    Inclui os campos `id`, `spot_number`, `is_occupied`, `created_at` e
    `updated_at`.

    """

    class Meta:
        model = ParkingSpot
        fields = ["id", *SPOT_FIELDS, "created_at", "updated_at"]


class PatchSpotSchema(ModelSchema):
    """Schema de atualização parcial para o ParkingSpot.

    Permite atualizar qualquer um dos campos `spot_number` ou `is_occupied`.
    Todos os campos são opcionais.

    """

    class Meta:
        model = ParkingSpot
        fields = SPOT_FIELDS
        fields_optional = SPOT_FIELDS


class FilterSpotSchema(FilterSchema):
    """Schema de filtro para consultas na model ParkingSpot.

    Permite filtrar por `spot_number` e `is_occupied`. O campo `spot_number`
    suporta buscas parciais (case-insensitive). O campo `is_occupied` é
    um filtro direto.

    """

    spot_number: Optional[str] = Field(None, q=["spot_number__icontains"])
    is_occupied: Optional[bool] = None
