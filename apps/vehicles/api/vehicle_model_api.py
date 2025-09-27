"""Módulo contendo as rotas relacionadas aos Modelos de veículos."""

from django.http import HttpRequest
from ninja import Query, Router

from utils.decorators import has_permissions_decorator
from utils.schemas import GenericMensageSchema
from utils.services import update_service

from ..models import VehicleModel
from ..schemas import (
    CreateVehicleModelSchema,
    FilterVehicleModelSchema,
    PatchVehicleModelSchema,
    VehicleModelSchema,
)

vehicle_models_router = Router(tags=["Modelos de veículos"])


@vehicle_models_router.post(
    path="/",
    response={
        201: VehicleModelSchema,
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Cria um Modelo de veículo no sistema.",
)
@has_permissions_decorator(["vehicles.add_vehiclemodel"])
def create_vehicle_model(
    request: HttpRequest, payload: CreateVehicleModelSchema
) -> tuple[int, VehicleModelSchema | GenericMensageSchema]:
    """Registra um Modelo de veículo no estacionamento.

    Verifica se o usuário tem a permissão `vehicles.add_vehiclemodel`.
    Se tiver, cria e persiste um novo objeto `VehicleModel`
    a partir do payload e retorna
    `(201, VehicleModelSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        payload (CreateVehicleModelSchema): dados enviados para criação do
        Modelo de veículo.

    Returns:
        tuple[int, VehicleModelSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        201: Modelo de veículo criado com sucesso.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        vehicle_model = VehicleModel.objects.create(**payload.dict())
        return 201, vehicle_model

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_models_router.delete(
    path="/{id}",
    response={
        200: GenericMensageSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Deleta o Modelo de veículo com id igual ao passado na url.",
)
@has_permissions_decorator(["vehicles.delete_vehiclemodel"])
def delete_vehicle_model(
    request: HttpRequest, id: int
) -> tuple[int, GenericMensageSchema]:
    """Deleta um Modelo de veículo do estacionamento.

    Verifica se o usuário tem a permissão `vehicles.delete_vehiclemodel`.
    Se tiver, deleta o `VehicleModel` com o id igual ao da url e retorna
    `(200, GenericMensageSchema)`. Se não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `VehicleModel`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do Modelo de veículo a ser deletado.

    Returns:
        tuple[int, GenericMensageSchema]: tupla contendo o status HTTP e o
        corpo da resposta.

    Responses:
        200: Modelo de veículo deletado com sucesso.
        403: Usuário não autorizado.
        404: Modelo de veículo não encontrado.
        500: Erro interno do servidor.

    """
    try:
        vehicle_model = VehicleModel.objects.get(id=id)
        vehicle_model.delete()

        return GenericMensageSchema.deleted_menssage("Modelo de Veículo")

    except VehicleModel.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage(
            "Modelo de Veículo"
        )

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_models_router.get(
    path="/",
    response={
        200: list[VehicleModelSchema],
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Devolve todos os Modelos de veículos cadastrados no sistema.",
)
@has_permissions_decorator(["vehicles.view_vehiclemodel"])
def get_vehicle_models(
    request: HttpRequest, filters: FilterVehicleModelSchema = Query(...)
) -> tuple[int, list[VehicleModelSchema] | GenericMensageSchema]:
    """Retorna todos os Modelos de veículos com base nos filtros.

    Verifica se o usuário tem a permissão `vehicles.view_vehiclemodel`.
    Se tiver, busca os `VehicleModel` e aplica os filtros. e retorna
    `(200, list[VehicleModelSchema])`. Se o usuário não tiver permissão,
    retorna `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        filters (FilterVehicleModelSchema, optional): filtros para a busca.

    Returns:
        tuple[int, list[VehicleModelSchema] | GenericMensageSchema]: tupla
        contendo o status HTTP e o corpo da resposta.

    Responses:
        200: Lista de Modelos de veículos.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        vehicle_models = VehicleModel.objects.all()
        if filters:
            vehicle_models = filters.filter(vehicle_models)

        return 200, vehicle_models

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_models_router.get(
    path="/{id}",
    response={
        200: VehicleModelSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Devolve o Modelo de veículo com id igual ao passado na url.",
)
@has_permissions_decorator(["vehicles.view_vehiclemodel"])
def get_vehicle_model(
    request: HttpRequest, id: int
) -> tuple[int, VehicleModelSchema | GenericMensageSchema]:
    """Retorna o Modelo de veículo com id igual ao da url.

    Verifica se o usuário tem a permissão `vehicles.view_vehiclemodel`.
    Se tiver, busca o `VehicleModel` com o mesmo id da url e retorna
    `(200, VehicleModelSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `VehicleModel`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do VehicleModel.

    Returns:
        tuple[int, VehicleModelSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Modelo de veículo com o mesmo id da url.
        403: Usuário não autorizado.
        404: Modelo de veículo não encontrado.
        500: Erro interno do servidor.

    """
    try:
        vehicle_model = VehicleModel.objects.get(id=id)
        return 200, vehicle_model

    except VehicleModel.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage(
            "Modelo de Veículo"
        )

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_models_router.patch(
    path="/{id}",
    response={
        200: VehicleModelSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Atualiza parcialmente um Modelo de veículo.",
)
@has_permissions_decorator(["vehicles.change_vehiclemodel"])
def patch_vehicle_model(
    request: HttpRequest, id: int, payload: PatchVehicleModelSchema
) -> tuple[int, VehicleModelSchema | GenericMensageSchema]:
    """Atualiza o Modelo de veículo com id igual ao da url.

    Verifica se o usuário tem a permissão `vehicles.change_vehiclemodel`.
    Se tiver, atualiza o `VehicleModel` com o id igual ao da url e retorna
    `(200, VehicleModelSchema)`. Se não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `VehicleModel`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do Modelo de veículo a ser atualizado.
        payload (PatchVehicleModelSchema): dados enviados para atualização do
        Modelo de veículo.

    Returns:
        tuple[int, VehicleModelSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Modelo de veículo atualizado com sucesso.
        403: Usuário não autorizado.
        404: Modelo de veículo não encontrado.
        500: Erro interno do servidor.

    """
    try:
        vehicle_model = VehicleModel.objects.get(id=id)

        update_service(payload, vehicle_model)
        vehicle_model.save()

        return 200, vehicle_model

    except VehicleModel.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage(
            "Modelo de Veículo"
        )

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()
