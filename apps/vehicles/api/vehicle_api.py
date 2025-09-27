"""Módulo contendo as rotas relacionadas aos Veículos."""

from django.http import HttpRequest
from ninja import Query, Router

from utils.decorators import has_permissions_decorator
from utils.schemas import GenericMensageSchema

from ..models import Vehicle
from ..schemas import (
    CreateVehicleSchema,
    FilterVehicleSchema,
    PatchVehicleSchema,
    VehicleSchema,
)
from ..services import update_vehicle

vehicles_router = Router(tags=["Vehicles"])


@vehicles_router.post(
    path="/",
    response={
        201: VehicleSchema,
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que registra um Veículo no estacionamento.",
)
@has_permissions_decorator(["vehicles.add_vehicle"])
def create_vehicle(
    request: HttpRequest, payload: CreateVehicleSchema
) -> tuple[int, VehicleSchema | GenericMensageSchema]:
    """Registra um Veículo no estacionamento.

    Verifica se o usuário tem a permissão `vehicles.add_vehicle`.
    Se tiver, cria e persiste um novo objeto `Vehicle`
    a partir do payload e retorna
    `(201, VehicleSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        payload (CreateVehicleSchema): dados enviados para criação do Veículo.

    Returns:
        tuple[int, VehicleSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        201: Veículo criado com sucesso.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        vehicle = Vehicle.objects.create(**payload.dict())

        return 201, vehicle

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicles_router.delete(
    path="/{id}",
    response={
        200: GenericMensageSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que deleta um Veículo do sistema.",
)
@has_permissions_decorator(["vehicles.delete_vehicle"])
def delete_vehicle(
    request: HttpRequest, id: int
) -> tuple[int, GenericMensageSchema]:
    """Deleta um Veículo do estacionamento.

    Verifica se o usuário tem a permissão `vehicles.delete_vehicle`.
    Se tiver, deleta o `Vehicle` com o id igual ao da url e retorna
    `(200, GenericMensageSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `Vehicle`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do Vehicle.

    Returns:
        tuple[int, GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Veículo deletado com sucesso.
        403: Usuário não autorizado.
        404: Veículo não encontrado.
        500: Erro interno do servidor.

    """
    try:
        vehicle = Vehicle.objects.get(id=id)
        vehicle.delete()

        return GenericMensageSchema.deleted_menssage("Veículo")

    except Vehicle.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Veículo")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicles_router.get(
    path="/",
    response={
        200: list[VehicleSchema],
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que devolve todos os Veículos do sistema.",
)
@has_permissions_decorator(["vehicles.view_vehicle"])
def get_vehicles(
    request: HttpRequest, filters: FilterVehicleSchema = Query(...)
) -> tuple[int, list[VehicleSchema] | GenericMensageSchema]:
    """Retorna todos os Veículos com base nos filtros.

    Verifica se o usuário tem a permissão `vehicles.view_vehicle`.
    Se tiver, busca os `Vehicle` e filtra eles com base em `filters`
    (a lista pode ser retornada vazia) e retorna
    `(200, list[VehicleSchema])`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        filters (FilterVehicleSchema): campos para filtrar as Vehicle.

    Returns:
        tuple[int, list[VehicleSchema | GenericMensageSchema]: tupla contendo
        o status HTTP e o corpo da resposta.

    Responses:
        200: Lista de Veículos.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        vehicles = Vehicle.objects.for_owner(request.user)

        if filters:
            vehicles = filters.filter(vehicles)

        return 200, vehicles

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicles_router.get(
    path="/{id}",
    response={
        200: VehicleSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que devolve um Veículo com id igual ao passado na url.",
)
@has_permissions_decorator(["vehicles.view_vehicle"])
def get_vehicle(
    request: HttpRequest, id: int
) -> tuple[int, VehicleSchema | GenericMensageSchema]:
    """Retorna o Veículo com id igual ao da url.

    Verifica se o usuário tem a permissão vehicles.view_vehicle`.
    Se tiver, busca o `Vehicle` com o mesmo id da url e retorna
    `(200, VehicleSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `Vehicle`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do Vehicle.

    Returns:
        tuple[int, VehicleSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Veículo com o mesmo id da url.
        403: Usuário não autorizado.
        404: Veículo não encontrado.
        500: Erro interno do servidor.

    """
    try:
        vehicle = Vehicle.objects.for_owner(request.user).get(id=id)

        return 200, vehicle

    except Exception:
        return 404, GenericMensageSchema.not_found_menssage("Veículo")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicles_router.patch(
    path="/{id}",
    response={
        200: VehicleSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que atualiza um Veículo.",
)
@has_permissions_decorator(["vehicles.change_vehicle"])
def patch_vehicle(
    request: HttpRequest, id: int, payload: PatchVehicleSchema
) -> tuple[int, VehicleSchema | GenericMensageSchema]:
    """Atualiza o Veículo com id igual ao da url.

    Verifica se o usuário tem a permissão `vehicles.change_vehicle`.
    Se tiver, busca o `Vehicle` com o mesmo id da url e o atualiza com
    base nos campos passados no payload e retorna
    `(200, VehicleSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `Vehicle`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do Vehicle.
        payload (PatchVehicleSchema): dados dos campos a serem atualizados.

    Returns:
        tuple[int, VehicleSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Veículo atualizado.
        403: Usuário não autorizado.
        404: Veículo não encontrado.
        500: Erro interno do servidor.

    """
    try:
        vehicle = Vehicle.objects.get(id=id)

        update_vehicle(payload, vehicle, save=True)

        return 200, vehicle

    except Vehicle.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Veículo")

    except Exception as e:
        print(e)
        return 500, GenericMensageSchema.internal_erro_menssage()
