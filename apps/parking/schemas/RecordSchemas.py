"""Schemas para o modelo ParkingRecord."""

from datetime import datetime
from typing import Optional

from ninja import Field, FilterSchema, ModelSchema, Schema

from ..models import ParkingRecord


class CreateRecordSchema(Schema):
    """Schema de criação para o ParkingRecord.

    Inclui os campos `vehicle_id`, `parking_spot_id`, `entry_time` e
    opcionalmente `exit_time`. O campo `exit_time` é opcional para permitir
    a criação de registros de entrada sem uma hora de saída imediata.

    """

    vehicle_id: Optional[int] = None
    parking_spot_id: Optional[int] = None


class RecordSchema(ModelSchema):
    """Schema de resposta para o ParkingRecord.

    Inclui os campos `id`, `vehicle`, `parking_spot`, `entry_time` e
    `exit_time`.
    """

    class Meta:
        model = ParkingRecord
        fields = ["id", "vehicle", "parking_spot", "entry_time", "exit_time"]


class PatchRecordSchema(ModelSchema):
    """Schema de atualização parcial para o ParkingRecord.

    Permite atualizar qualquer um dos campos `exit_time`, `vehicle_id` ou
    `parking_spot_id`. Todos os campos são opcionais.

    """

    vehicle_id: Optional[int] = None
    parking_spot_id: Optional[int] = None

    class Meta:
        model = ParkingRecord
        fields = ["exit_time"]
        fields_optional = ["exit_time"]


class FilterRecordSchema(FilterSchema):
    """Schema de filtro para consultas na model ParkingRecord.

    Permite filtrar por `license_plate`, `spot_number`, `entry_time` e
    `exit_time`. Os campos `license_plate` e `spot_number` suportam
    buscas parciais (case-insensitive). Os campos `entry_time` e `exit_time`
    são filtros diretos.

    """

    license_plate: Optional[str] = Field(
        None, q=["vehicle__license_plate__icontains"]
    )
    spot_number: Optional[str] = Field(
        None, q=["parking_spot__spot_number__icontains"]
    )
    entry_time: Optional[datetime] = None
    exit_time: Optional[datetime] = None
