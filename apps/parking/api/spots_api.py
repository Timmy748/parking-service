"""Módulo que contém as rotas relacionadas às Vagas do estacionamento."""

from django.http import HttpRequest
from ninja import Query, Router

from utils.decorators import has_permissions_decorator
from utils.schemas import GenericMensageSchema
from utils.services import update_service

from ..models import ParkingSpot
from ..schemas import (
    CreateSpotSchema,
    FilterSpotSchema,
    PatchSpotSchema,
    SpotSchema,
)

spots_router = Router(tags=["Vagas"])


@spots_router.post(
    path="/",
    response={
        201: SpotSchema,
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que registra uma vaga no estacionamento.",
)
@has_permissions_decorator(["parking.add_parkingspot"])
def create_spot(
    request: HttpRequest, payload: CreateSpotSchema
) -> tuple[int, SpotSchema | GenericMensageSchema]:
    """Cria uma Vaga no estacionamento.

    Verifica se o usuário tem a permissão `parking.add_parkingspot`.
    Se tiver, cria e persiste um novo objeto `ParkingSpot`
    a partir do payload e retorna
    `(201, SpotSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        payload (CreateSpotSchema): dados enviados para criação da Vaga.

    Returns:
        tuple[int, SpotSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        201: Vaga criada com sucesso.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        spot = ParkingSpot.objects.create(**payload.dict())

        return 201, spot

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@spots_router.delete(
    path="/{id}",
    response={
        200: GenericMensageSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que deleta a Vaga com id passado na url.",
)
@has_permissions_decorator(["parking.delete_parkingspot"])
def delete_spot(
    request: HttpRequest, id: int
) -> tuple[int, GenericMensageSchema]:
    """Deleta uma Vaga do estacionamento.

    Verifica se o usuário tem a permissão `parking.delete_parkingspot`.
    Se tiver, deleta o `ParkingSpot` com o id igual ao da url e retorna
    `(200, GenericMensageSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `ParkingSpot`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do ParkingSpot.

    Returns:
        tuple[int, GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Vaga deletada com sucesso.
        403: Usuário não autorizado.
        404: Vaga não encontrada.
        500: Erro interno do servidor.

    """
    try:
        spot = ParkingSpot.objects.get(id=id)
        spot.delete()

        return 200, GenericMensageSchema.deleted_menssage("Vaga")

    except ParkingSpot.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Vaga")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@spots_router.get(
    path="/",
    response={
        200: list[SpotSchema],
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que devolve todas as Vagas do estacionamento.",
)
@has_permissions_decorator(["parking.view_parkingspot"])
def get_spots(
    request: HttpRequest, filters: FilterSpotSchema = Query(...)
) -> tuple[int, list[SpotSchema] | GenericMensageSchema]:
    """Retorna todos as Vagas com base nos filtros.

    Verifica se o usuário tem a permissão `parking.view_parkingspot`.
    Se tiver, busca os `ParkingSpots` e filtra eles com base em `filters`
    (a lista pode ser retornada vazia) e retorna
    `(200, list[SpotSchema])`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        filters (FilterSpotSchema): campos para filtrar as ParkingSpot.

    Returns:
        tuple[int, list[RecordSchema | GenericMensageSchema]: tupla contendo
        o status HTTP e o corpo da resposta.

    Responses:
        200: Lista de Vagas.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        spots = ParkingSpot.objects.all()

        if filters:
            spots = filters.filter(spots)

        return 200, spots

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@spots_router.get(
    path="/{id}",
    response={
        200: SpotSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que devolve a Vaga com id igual ao passado na url.",
)
@has_permissions_decorator(["parking.view_parkingspot"])
def get_spot(
    request: HttpRequest, id: int
) -> tuple[int, SpotSchema | GenericMensageSchema]:
    """Retorna a Vaga com id igual ao da url.

    Verifica se o usuário tem a permissão `parking.view_parkingspot`.
    Se tiver, busca o `ParkingSpot` com o mesmo id da url e retorna
    `(200, SpotSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `ParkingSpot`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id da Vaga.

    Returns:
        tuple[int, SpotSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Vaga com o mesmo id da url.
        403: Usuário não autorizado.
        404: Vaga não encontrada.
        500: Erro interno do servidor.

    """
    try:
        spot = ParkingSpot.objects.get(id=id)

        return 200, spot

    except ParkingSpot.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Vaga")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@spots_router.patch(
    path="/spots/{id}",
    response={
        200: SpotSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que atualiza parcialmente a vaga.",
)
@has_permissions_decorator(["parking.change_parkingspot"])
def patch_spot(
    request: HttpRequest, id: int, payload: PatchSpotSchema
) -> tuple[int, SpotSchema | GenericMensageSchema]:
    """Atualiza a Vaga com id igual ao da url.

    Verifica se o usuário tem a permissão `parking.change_parkingspot`.
    Se tiver, busca o `ParkingSpot` com o mesmo id da url e o atualiza com
    base nos campos passados no payload e retorna
    `(200, SpotSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `ParkingSpot`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do ParkingSpot.
        payload (PatchSpotSchema): dados dos campos a serem atualizados.

    Returns:
        tuple[int, SpotSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Vaga atualizada.
        403: Usuário não autorizado.
        404: Vaga não encontrada.
        500: Erro interno do servidor.

    """
    try:
        spot = ParkingSpot.objects.get(id=id)

        update_service(payload, spot)

        spot.save()

        return 200, spot

    except ParkingSpot.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Vaga")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()
