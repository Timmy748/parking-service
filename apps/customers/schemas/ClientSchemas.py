"""Schemas para a model Customer."""

from datetime import datetime
from typing import Optional

from ninja import Field, FilterSchema, ModelSchema

from ..models import Customer

CUSTOMER_FIELDS = ["name", "phone", "cpf"]


class CreateCustomerSchema(ModelSchema):
    """Schema de criação para o Customer.

    Inclui os campos `name`, `phone`, `cpf` e opcionalmente `user_id`.
    O campo `user_id` é opcional para permitir a criação de clientes sem
    associação a um usuário.

    """

    user_id: Optional[int] = None

    class Meta:
        model = Customer
        fields = CUSTOMER_FIELDS
        fields_optional = ["phone", "cpf"]


class CustomerSchema(ModelSchema):
    """Schema de resposta para o Customer.

    Inclui os campos `id`, `user`, "name", "phone", "cpf", `created_at` e
    `updated_at`.

    """

    class Meta:
        model = Customer
        fields = ["id", "user", *CUSTOMER_FIELDS, "created_at", "updated_at"]


class PatchCustomerSchema(ModelSchema):
    """Schema de atualização parcial para o Customer.

    Permite atualizar qualquer um dos campos `name`, `phone` ou `cpf`.
    Todos os campos são opcionais.

    """

    class Meta:
        model = Customer
        fields = CUSTOMER_FIELDS
        fields_optional = CUSTOMER_FIELDS


class FilterCustomerSchema(FilterSchema):
    """Schema de filtro para consultas na model Customer.

    Permite filtrar por `name`, `phone`, `cpf`, `created_at` e `updated_at`.
    Os campos `name`, `phone` e `cpf` suportam buscas parciais
    (case-insensitive).
    Os campos `created_at` e `updated_at` são filtros diretos.

    """

    name: Optional[str] = Field(None, q=["name__icontains"])
    phone: Optional[str] = Field(None, q=["phone__icontains"])
    cpf: Optional[str] = Field(None, q=["cpf__icontains"])
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
