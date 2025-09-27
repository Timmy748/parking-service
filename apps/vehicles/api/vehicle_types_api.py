"""Módulo contendo as rotas relacionadas aos Tipos de veículos."""

from django.http import HttpRequest
from ninja import Query, Router

from utils.decorators import has_permissions_decorator
from utils.schemas import GenericMensageSchema
from utils.services import update_service

from ..models import VehicleType
from ..schemas import (
    CreateVehicleTypeSchema,
    FilterVehicleTypeSchema,
    PatchVehicleTypeSchema,
    VehicleTypeSchema,
)

vehicle_types_router = Router(tags=["Tipos de veículos"])


@vehicle_types_router.post(
    path="/",
    response={
        201: VehicleTypeSchema,
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Cria um Tipo de veículo no sistema.",
)
@has_permissions_decorator(["vehicles.add_vehicletype"])
def create_vehicle_type(
    request: HttpRequest, payload: CreateVehicleTypeSchema
) -> tuple[int, VehicleTypeSchema | GenericMensageSchema]:
    """Registra um Tipo de veículo no estacionamento.

    Verifica se o usuário tem a permissão `vehicles.add_vehicletype`.
    Se tiver, cria e persiste um novo objeto `Vehicle`
    a partir do payload e retorna
    `(201, VehicleTypeSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        payload (CreateVehicleTypeSchema): dados enviados para criação do
        Tipo de veículo.

    Returns:
        tuple[int, VehicleTypeSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        201: Tipo de veículo criado com sucesso.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        vehicle_type = VehicleType.objects.create(**payload.dict())

        return 201, vehicle_type

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_types_router.delete(
    path="/{id}",
    response={
        200: GenericMensageSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Deleta o Tipo de veículo com id igual ao passado na url.",
)
@has_permissions_decorator(["vehicles.delete_vehicletype"])
def delete_vehicle_type(
    request: HttpRequest, id: int
) -> tuple[int, GenericMensageSchema]:
    """Deleta um Tipo de veículo do estacionamento.

    Verifica se o usuário tem a permissão `vehicles.delete_vehicletype`.
    Se tiver, deleta o `VehicleType` com o id igual ao da url e retorna
    `(200, GenericMensageSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `VehicleType`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do VehicleType.

    Returns:
        tuple[int, GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Tipo de veículo deletado com sucesso.
        403: Usuário não autorizado.
        404: Tipo de veículo não encontrado.
        500: Erro interno do servidor.

    """
    try:
        vehicle_type = VehicleType.objects.get(id=id)
        vehicle_type.delete()

        return GenericMensageSchema.deleted_menssage("Tipo De Veículo")

    except VehicleType.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Tipo De Veículo")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_types_router.get(
    path="/",
    response={
        200: list[VehicleTypeSchema],
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Devolve todos os Tipos de veículos cadastrados no sistema.",
)
@has_permissions_decorator(["vehicles.view_vehicletype"])
def get_vehicles_type(
    request: HttpRequest, filters: FilterVehicleTypeSchema = Query(...)
) -> tuple[int, list[VehicleTypeSchema] | GenericMensageSchema]:
    """Retorna todos os Tipos de veículos com base nos filtros.

    Verifica se o usuário tem a permissão `vehicles.view_vehicletype`.
    Se tiver, busca os `VehicleType` e filtra eles com base em `filters`
    (a lista pode ser retornada vazia) e retorna
    `(200, list[VehicleTypeSchema])`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        filters (FilterVehicleTypeSchema): campos para filtrar as VehicleType.

    Returns:
        tuple[int, list[VehicleTypeSchema | GenericMensageSchema]: tupla
        contendo o status HTTP e o corpo da resposta.

    Responses:
        200: Lista de Tipos de veículos.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        vehicles_type = VehicleType.objects.all()
        if filters:
            vehicles_type = filters.filter(vehicles_type)

        return 200, vehicles_type

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_types_router.get(
    path="/{id}",
    response={
        200: VehicleTypeSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Devolve o Tipo de veículo com id igual ao passado na url.",
)
@has_permissions_decorator(["vehicles.view_vehicletype"])
def get_vehicle_type(
    request: HttpRequest, id: int
) -> tuple[int, VehicleTypeSchema | GenericMensageSchema]:
    """Retorna o Tipo de veículo com id igual ao da url.

    Verifica se o usuário tem a permissão vehicles.view_vehicletype`.
    Se tiver, busca o `VehicleType` com o mesmo id da url e retorna
    `(200, VehicleTypeSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `VehicleType`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do VehicleType.

    Returns:
        tuple[int, VehicleTypeSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Tipo de veículo com o mesmo id da url.
        403: Usuário não autorizado.
        404: Tipo de veículo não encontrado.
        500: Erro interno do servidor.

    """
    try:
        vehicles_type = VehicleType.objects.get(id=id)

        return 200, vehicles_type

    except Exception:
        return 404, GenericMensageSchema.not_found_menssage("Tipo De Veículo")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_types_router.patch(
    path="/{id}",
    response={
        200: VehicleTypeSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Atualiza parcialmente um Tipo de veículo.",
)
@has_permissions_decorator(["vehicles.change_vehicletype"])
def patch_vehicle_type(
    request: HttpRequest, id: int, payload: PatchVehicleTypeSchema
) -> tuple[int, VehicleTypeSchema | GenericMensageSchema]:
    """Atualiza o Tipo de veículo com id igual ao da url.

    Verifica se o usuário tem a permissão `vehicles.change_vehicle`.
    Se tiver, busca o `VehicleType` com o mesmo id da url e o atualiza com
    base nos campos passados no payload e retorna
    `(200, VehicleTypeSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `VehicleType`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do VehicleType.
        payload (PatchVehicleTypeSchema): dados dos campos a serem atualizados.

    Returns:
        tuple[int, VehicleTypeSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Tipo de veículo atualizado.
        403: Usuário não autorizado.
        404: Tipo de veículo não encontrado.
        500: Erro interno do servidor.

    """
    try:
        vehicle_type = VehicleType.objects.get(id=id)

        update_service(payload, vehicle_type)

        vehicle_type.save()

        return 200, vehicle_type

    except VehicleType.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Tipo De Veículo")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()
