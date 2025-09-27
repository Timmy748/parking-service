"""Módulo contendo as rotas relacionadas aos Clientes."""

from django.http import HttpRequest
from ninja import Query, Router

from utils.decorators import has_permissions_decorator
from utils.schemas import GenericMensageSchema
from utils.services import update_service

from ..models import Customer
from ..schemas import (
    CreateCustomerSchema,
    CustomerSchema,
    FilterCustomerSchema,
    PatchCustomerSchema,
)

customer_router = Router(tags=["Cliente"])


@customer_router.post(
    path="/",
    response={
        201: CustomerSchema,
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota para registrar um novo cliente.",
)
@has_permissions_decorator(["customers.add_customer"])
def create_customer(
    request: HttpRequest, payload: CreateCustomerSchema
) -> tuple[int, CustomerSchema | GenericMensageSchema]:
    """Cria um novo cliente.

    Verifica se o usuário tem a permissão `customers.add_customer`. Se tiver,
    cria e persiste um novo objeto `Customer` a partir do payload e retorna
    `(201, CustomerSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        payload (CreateCustomerSchema): dados enviados para criação do Cliente.

    Returns:
        tuple[int, CustomerSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        201: Cliente criado com sucesso.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        customer = Customer.objects.create(**payload.dict())

        return 201, customer

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@customer_router.delete(
    "/{id}",
    response={
        200: GenericMensageSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que Deleta o Customer com id passado na url.",
)
@has_permissions_decorator(["customers.delete_customer"])
def delete_customer(
    request: HttpRequest, id: int
) -> tuple[int, GenericMensageSchema]:
    """Deleta um Cliente.

    Verifica se o usuário tem a permissão `customers.delete_customer`.
    Se tiver, deleta o `Customer` com o id igual ao da url e retorna
    `(200, GenericMensageSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `Customer`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do Customer.

    Returns:
        tuple[int, GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Cliente deletado com sucesso.
        403: Usuário não autorizado.
        404: Cliente não encontrado.
        500: Erro interno do servidor.

    """
    try:
        customer = Customer.objects.get(id=id)
        customer.delete()

        return 200, GenericMensageSchema.deleted_menssage("Cliente")

    except Customer.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Cliente")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@customer_router.get(
    "/",
    response={
        200: list[CustomerSchema],
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que devolve todas os registro da tabela Customers.",
)
@has_permissions_decorator(["customers.view_customer"])
def get_customers(
    request: HttpRequest, filters: FilterCustomerSchema = Query(None)
) -> tuple[int, list[CustomerSchema] | GenericMensageSchema]:
    """Retorna todos os Clientes com base nos filtros.

    Verifica se o usuário tem a permissão `customers.view_customer`.
    Se tiver, busca os `Customers` e filtra eles com base em `filters`
    (a lista pode ser retornada vazia) e retorna
    `(200, list[CustomerSchema])`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        filters (FilterCustomerSchema): campos para filtrar os Customers.

    Returns:
        tuple[int, list[CustomerSchema | GenericMensageSchema]: tupla contendo
        o status HTTP e o corpo da resposta.

    Responses:
        200: Lista de Clientes.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        customers = Customer.objects.filter()

        if filters:
            customers = filters.filter(customers)

        return 200, customers

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@customer_router.get(
    "/{id}",
    response={
        200: CustomerSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que devolve o Customer com id passado na url.",
)
@has_permissions_decorator(["customers.view_customer"])
def get_customer(
    request: HttpRequest, id: int
) -> tuple[int, CustomerSchema | GenericMensageSchema]:
    """Retorna o Cliente com id igual ao da url.

    Verifica se o usuário tem a permissão `customers.view_customer`.
    Se tiver, busca o `Customer` com o mesmo id da url e retorna
    `(200, CustomerSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `Customer`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do Customer.

    Returns:
        tuple[int, CustomerSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Cliente com o mesmo id da url.
        403: Usuário não autorizado.
        404: Cliente não encontrado.
        500: Erro interno do servidor.

    """
    try:
        customer = Customer.objects.get(id=id)

        return 200, customer

    except Customer.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Cliente")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@customer_router.patch(
    "/{id}",
    response={
        200: CustomerSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Atualiza parcialmente um Customer.",
)
@has_permissions_decorator(["customers.change_customer"])
def patch_customer(
    request: HttpRequest, id: int, payload: PatchCustomerSchema
) -> tuple[int, CustomerSchema | GenericMensageSchema]:
    """Atualiza o Cliente com id igual ao da url.

    Verifica se o usuário tem a permissão `customers.change_customer`.
    Se tiver, busca o `Customer` com o mesmo id da url e o atualiza com
    base nos campos passados no payload e retorna
    `(200, CustomerSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `Customer`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do Customer.
        payload (PatchCustomerSchema): dados dos campos a serem atualizados.

    Returns:
        tuple[int, CustomerSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Cliente atualizado.
        403: Usuário não autorizado.
        404: Cliente não encontrado.
        500: Erro interno do servidor.

    """
    try:
        customer: Customer = Customer.objects.get(id=id)

        update_service(payload, customer)

        customer.save()

        return 200, customer

    except Customer.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Cliente")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()
