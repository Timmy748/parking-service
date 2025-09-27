"""Schemas para a model Vehicle."""

from ninja import Field, FilterSchema, ModelSchema

from ..models import Vehicle


class CreateVehicleSchema(ModelSchema):
    """Schema de criação para o Vehicle.

    Inclui os campos `vehicle_type_id`, `owner_id`, `license_plate`, `brand`,
    `model` e `color`.

    """

    vehicle_type_id: int | None = None
    owner_id: int | None = None

    class Meta:
        model = Vehicle
        fields = [
            "license_plate",
            "brand",
            "model",
            "color",
        ]


class VehicleSchema(ModelSchema):
    """Schema de resposta para o Vehicle.

    Inclui os campos `id`, `vehicle_type`, `owner`, `license_plate`, `brand`,
    `model`, `color`, `created_at` e `updated_at`.

    """

    vehicle_type: str | None = Field(None, alias="vehicle_type.name")
    brand: str | None = Field(None, alias="brand.name")
    model: str | None = Field(None, alias="model.name")
    color: str | None = Field(None, alias="color.name")

    class Meta:
        model = Vehicle
        fields = [
            "id",
            "owner",
            "license_plate",
            "created_at",
            "updated_at",
        ]


class PatchVehicleSchema(ModelSchema):
    """Schema de atualização parcial para o Vehicle.

    Permite atualizar qualquer um dos campos `vehicle_type`, `owner_id`,
    `license_plate`, `brand`, `model` ou `color`. Todos os campos são
    opcionais.

    """

    owner_id: int | None = None
    vehicle_type: str | int | None = None
    brand: str | int | None = None
    model: str | int | None = None
    color: str | int | None = None

    class Meta:
        model = Vehicle
        fields = ["license_plate"]
        fields_optional = ["license_plate"]


class FilterVehicleSchema(FilterSchema):
    """Schema de filtro para consultas na model Vehicle.

    Permite filtrar por `vehicle_type`, `license_plate`, `brand`, `model` e
    `color`. Todos os campos suportam buscas parciais (case-insensitive).

    """

    vehicle_type: str | None = Field(None, q=["vehicle_type__name__icontains"])
    license_plate: str | None = Field(None, q=["license_plate__icontains"])
    brand: str | None = Field(None, q=["brand__name__icontains"])
    model: str | None = Field(None, q=["model__name__icontains"])
    color: str | None = Field(None, q=["color__name__icontains"])
