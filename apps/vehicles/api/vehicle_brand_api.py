"""Módulo contendo as rotas relacionadas às Marcas de veículos."""

from django.http import HttpRequest
from ninja import Query, Router

from utils.decorators import has_permissions_decorator
from utils.schemas import GenericMensageSchema
from utils.services import update_service

from ..models import VehicleBrand
from ..schemas import (
    CreateVehicleBrandSchema,
    FilterVehicleBrandSchema,
    PatchVehicleBrandSchema,
    VehicleBrandSchema,
)

vehicle_brands_router = Router(tags=["Marcas de veículos"])


@vehicle_brands_router.post(
    path="/",
    response={
        201: VehicleBrandSchema,
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Cria uma Marca de veículo no sistema.",
)
@has_permissions_decorator(["vehicles.add_vehiclebrand"])
def create_vehicle_brand(
    request: HttpRequest, payload: CreateVehicleBrandSchema
) -> tuple[int, VehicleBrandSchema | GenericMensageSchema]:
    """Registra uma Marca de veículo no estacionamento.

    Verifica se o usuário tem a permissão `vehicles.add_vehiclebrand`.
    Se tiver, cria e persiste um novo objeto `VehicleBrand`
    a partir do payload e retorna
    `(201, VehicleBrandSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        payload (CreateVehicleBrandSchema): dados enviados para criação da
        Marca de veículo.

    Returns:
        tuple[int, VehicleBrandSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        201: Marca de veículo criada com sucesso.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        vehicle_brand = VehicleBrand.objects.create(**payload.dict())
        return 201, vehicle_brand

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_brands_router.delete(
    path="/{id}",
    response={
        200: GenericMensageSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Deleta a Marca de veículo com id igual ao passado na url.",
)
@has_permissions_decorator(["vehicles.delete_vehiclebrand"])
def delete_vehicle_brand(
    request: HttpRequest, id: int
) -> tuple[int, GenericMensageSchema]:
    """Deleta uma Marca de veículo do estacionamento.

    Verifica se o usuário tem a permissão `vehicles.delete_vehiclebrand`.
    Se tiver, deleta o `VehicleBrand` com o id igual ao da url e retorna
    `(200, GenericMensageSchema)`. Se não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `VehicleBrand`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id da Marca de veículo a ser deletada.

    Returns:
        tuple[int, GenericMensageSchema]: tupla contendo o status HTTP e o
        corpo da resposta.

    Responses:
        200: Marca de veículo deletada com sucesso.
        403: Usuário não autorizado.
        404: Marca de veículo não encontrada.
        500: Erro interno do servidor.

    """
    try:
        vehicle_brand = VehicleBrand.objects.get(id=id)
        vehicle_brand.delete()

        return GenericMensageSchema.deleted_menssage("Marca de Veículo")

    except VehicleBrand.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Marca de Veículo")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_brands_router.get(
    path="/",
    response={
        200: list[VehicleBrandSchema],
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Devolve todas as Marcas de veículos cadastradas no sistema.",
)
@has_permissions_decorator(["vehicles.view_vehiclebrand"])
def get_vehicle_brands(
    request: HttpRequest, filters: FilterVehicleBrandSchema = Query(...)
) -> tuple[int, list[VehicleBrandSchema] | GenericMensageSchema]:
    """Retorna todas as Marcas de veículos com base nos filtros.

    Verifica se o usuário tem a permissão `vehicles.view_vehiclebrand`.
    Se tiver, busca os `VehicleBrand` e aplica os filtros. e retorna
    `(200, list[VehicleBrandSchema])`. Se o usuário não tiver permissão,
    retorna `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        filters (FilterVehicleBrandSchema, optional): filtros para a busca.

    Returns:
        tuple[int, list[VehicleBrandSchema] | GenericMensageSchema]: tupla
        contendo o status HTTP e o corpo da resposta.

    Responses:
        200: Lista de Marcas de veículos.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        vehicle_brands = VehicleBrand.objects.all()
        if filters:
            vehicle_brands = filters.filter(vehicle_brands)

        return 200, vehicle_brands

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_brands_router.get(
    path="/{id}",
    response={
        200: VehicleBrandSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Devolve a Marca de veículo com id igual ao passado na url.",
)
@has_permissions_decorator(["vehicles.view_vehiclebrand"])
def get_vehicle_brand(
    request: HttpRequest, id: int
) -> tuple[int, VehicleBrandSchema | GenericMensageSchema]:
    """Retorna a Marca de veículo com id igual ao da url.

    Verifica se o usuário tem a permissão `vehicles.view_vehiclebrand`.
    Se tiver, busca o `VehicleBrand` com o mesmo id da url e retorna
    `(200, VehicleBrandSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `VehicleBrand`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do VehicleBrand.

    Returns:
        tuple[int, VehicleBrandSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Marca de veículo com o mesmo id da url.
        403: Usuário não autorizado.
        404: Marca de veículo não encontrada.
        500: Erro interno do servidor.

    """
    try:
        vehicle_brand = VehicleBrand.objects.get(id=id)
        return 200, vehicle_brand

    except VehicleBrand.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Marca de Veículo")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@vehicle_brands_router.patch(
    path="/{id}",
    response={
        200: VehicleBrandSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Atualiza parcialmente uma Marca de veículo.",
)
@has_permissions_decorator(["vehicles.change_vehiclebrand"])
def patch_vehicle_brand(
    request: HttpRequest, id: int, payload: PatchVehicleBrandSchema
) -> tuple[int, VehicleBrandSchema | GenericMensageSchema]:
    """Atualiza a Marca de veículo com id igual ao da url.

    Verifica se o usuário tem a permissão `vehicles.change_vehiclebrand`.
    Se tiver, atualiza o `VehicleBrand` com o id igual ao da url e retorna
    `(200, VehicleBrandSchema)`. Se não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `VehicleBrand`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id da Marca de veículo a ser atualizada.
        payload (PatchVehicleBrandSchema): dados enviados para atualização da
        Marca de veículo.

    Returns:
        tuple[int, VehicleBrandSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Marca de veículo atualizada com sucesso.
        403: Usuário não autorizado.
        404: Marca de veículo não encontrada.
        500: Erro interno do servidor.

    """
    try:
        vehicle_brand = VehicleBrand.objects.get(id=id)

        update_service(payload, vehicle_brand)
        vehicle_brand.save()

        return 200, vehicle_brand

    except VehicleBrand.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Marca de Veículo")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()
