"""Módulo contendo as rotas relacionadas ás Cores de veículos."""

from django.http import HttpRequest
from ninja import Query, Router

from utils.decorators import has_permissions_decorator
from utils.schemas import GenericMensageSchema

from ..models import VehicleColor
from ..schemas import (
    CreateVehicleColorSchema,
    FilterVehicleColorSchema,
    PatchVehicleColorSchema,
    VehicleColorSchema,
)

vehicle_colors_router = Router(tags=["Cores de veículos"])


@vehicle_colors_router.post(
    path="/",
    response={
        201: VehicleColorSchema,
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Cria uma Cor de veículo no sistema.",
)
@has_permissions_decorator(["vehicles.add_vehiclecolor"])
def create_vehicle_color(
    request: HttpRequest, payload: CreateVehicleColorSchema
) -> tuple[int, VehicleColorSchema | GenericMensageSchema]:
    """Registra uma Cor de veículo no estacionamento.

    Verifica se o usuário tem a permissão `vehicles.add_vehiclecolor`.
    Se tiver, cria e persiste um novo objeto `VehicleColor`
    a partir do payload e retorna
    `(201, VehicleColorSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        payload (CreateVehicleColorSchema): dados enviados para criação da
        Cor de veículo.

    Returns:
        tuple[int, VehicleColorSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        201: Cor de veículo criada com sucesso.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        vehicle_color = VehicleColor.objects.create(**payload.dict())
        return 201, vehicle_color

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_colors_router.delete(
    path="/{id}",
    response={
        200: GenericMensageSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Deleta a Cor de veículo com id igual ao passado na url.",
)
@has_permissions_decorator(["vehicles.delete_vehiclecolor"])
def delete_vehicle_color(
    request: HttpRequest, id: int
) -> tuple[int, GenericMensageSchema]:
    """Deleta uma Cor de veículo do estacionamento.

    Verifica se o usuário tem a permissão `vehicles.delete_vehiclecolor`.
    Se tiver, deleta o `VehicleColor` com o id igual ao da url e retorna
    `(200, GenericMensageSchema)`. Se não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `VehicleColor`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id da Cor de veículo a ser deletada.

    Returns:
        tuple[int, GenericMensageSchema]: tupla contendo o status HTTP e o
        corpo da resposta.

    Responses:
        200: Cor de veículo deletada com sucesso.
        403: Usuário não autorizado.
        404: Cor de veículo não encontrada.
        500: Erro interno do servidor.

    """
    try:
        vehicle_color = VehicleColor.objects.get(id=id)
        vehicle_color.delete()

        return GenericMensageSchema.deleted_menssage("Cor de Veículo")

    except VehicleColor.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Cor de Veículo")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_colors_router.get(
    path="/",
    response={
        200: list[VehicleColorSchema],
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Devolve todas as Cores de veículos cadastradas no sistema.",
)
@has_permissions_decorator(["vehicles.view_vehiclecolor"])
def get_vehicle_colors(
    request: HttpRequest, filters: FilterVehicleColorSchema = Query(...)
) -> tuple[int, list[VehicleColorSchema] | GenericMensageSchema]:
    """Retorna todas as Cores de veículos com base nos filtros.

    Verifica se o usuário tem a permissão `vehicles.view_vehiclecolor`.
    Se tiver, busca os `VehicleColor` e aplica os filtros. e retorna
    `(200, list[VehicleColorSchema])`. Se o usuário não tiver permissão,
    retorna `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        filters (FilterVehicleColorSchema, optional): filtros para a busca.

    Returns:
        tuple[int, list[VehicleColorSchema] | GenericMensageSchema]: tupla
        contendo o status HTTP e o corpo da resposta.

    Responses:
        200: Lista de Cores de veículos.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        vehicle_colors = VehicleColor.objects.all()
        if filters:
            vehicle_colors = filters.filter(vehicle_colors)

        return 200, vehicle_colors

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_colors_router.get(
    path="/{id}",
    response={
        200: VehicleColorSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Devolve a Cor de veículo com id igual ao passado na url.",
)
@has_permissions_decorator(["vehicles.view_vehiclecolor"])
def get_vehicle_color(
    request: HttpRequest, id: int
) -> tuple[int, VehicleColorSchema | GenericMensageSchema]:
    """Retorna a Cor de veículo com id igual ao da url.

    Verifica se o usuário tem a permissão `vehicles.view_vehiclecolor`.
    Se tiver, busca o `VehicleColor` com o mesmo id da url e retorna
    `(200, VehicleColorSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `VehicleColor`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do VehicleColor.

    Returns:
        tuple[int, VehicleColorSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Cor de veículo com o mesmo id da url.
        403: Usuário não autorizado.
        404: Cor de veículo não encontrada.
        500: Erro interno do servidor.

    """
    try:
        vehicle_color = VehicleColor.objects.get(id=id)
        return 200, vehicle_color

    except VehicleColor.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Cor de Veículo")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_colors_router.patch(
    path="/{id}",
    response={
        200: VehicleColorSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Atualiza parcialmente uma Cor de veículo.",
)
@has_permissions_decorator(["vehicles.change_vehiclecolor"])
def patch_vehicle_color(
    request: HttpRequest, id: int, payload: PatchVehicleColorSchema
) -> tuple[int, VehicleColorSchema | GenericMensageSchema]:
    """Atualiza a Cor de veículo com id igual ao da url.

    Verifica se o usuário tem a permissão `vehicles.change_vehiclecolor`.
    Se tiver, atualiza o `VehicleColor` com o id igual ao da url e retorna
    `(200, VehicleColorSchema)`. Se não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `VehicleColor`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id da Cor de veículo a ser atualizada.
        payload (PatchVehicleColorSchema): dados enviados para atualização da
        Cor de veículo.

    Returns:
        tuple[int, VehicleColorSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Cor de veículo atualizada com sucesso.
        403: Usuário não autorizado.
        404: Cor de veículo não encontrada.
        500: Erro interno do servidor.

    """
    try:
        vehicle_color = VehicleColor.objects.get(id=id)

        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(vehicle_color, attr, value)
        vehicle_color.save()

        return 200, vehicle_color

    except VehicleColor.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Cor de Veículo")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()
