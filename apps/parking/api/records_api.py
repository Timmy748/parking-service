"""Módulo contendo as rotas relacionadas aos Registros do estacionamento."""

from django.http import HttpRequest
from ninja import Query, Router

from utils.decorators import has_permissions_decorator
from utils.schemas import GenericMensageSchema
from utils.services import update_service

from ..models import ParkingRecord
from ..schemas import (
    CreateRecordSchema,
    FilterRecordSchema,
    PatchRecordSchema,
    RecordSchema,
)

records_router = Router(tags=["Registros"])


@records_router.post(
    path="/",
    response={
        201: RecordSchema,
        403: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que cria um Registro no estacionamento.",
)
@has_permissions_decorator(["parking.add_parkingrecord"])
def create_record(
    request: HttpRequest, payload: CreateRecordSchema
) -> tuple[int, RecordSchema | GenericMensageSchema]:
    """Cria um Registro no estacionamento.

    Verifica se o usuário tem a permissão `parking.add_parkingrecord`.
    Se tiver, cria e persiste um novo objeto `ParkingRecord`
    a partir do payload e retorna
    `(201, RecordSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        payload (CreateRecordSchema): dados enviados para criação do Registro.

    Returns:
        tuple[int, RecordSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        201: Registro criado com sucesso.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        record = ParkingRecord.objects.create(**payload.dict())

        return 201, record

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@records_router.delete(
    path="/{id}",
    response={
        200: GenericMensageSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que deleta o Registro com id passado na url.",
)
@has_permissions_decorator(["parking.delete_parkingrecord"])
def delete_record(
    request: HttpRequest, id: int
) -> tuple[int, GenericMensageSchema]:
    """Deleta um Registro do estacionamento.

    Verifica se o usuário tem a permissão `parking.delete_parkingrecord`.
    Se tiver, deleta o `ParkingRecord` com o id igual ao da url e retorna
    `(200, GenericMensageSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `ParkingRecord`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do ParkingRecord.

    Returns:
        tuple[int, GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Registro deletado com sucesso.
        403: Usuário não autorizado.
        404: Registro não encontrado.
        500: Erro interno do servidor.

    """
    try:
        record = ParkingRecord.objects.get(id=id)
        record.delete()

        return GenericMensageSchema.deleted_menssage("Registro")

    except ParkingRecord.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Registro")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@records_router.get(
    path="/",
    response={
        200: list[RecordSchema],
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que devolve todos os Registros do estacionamento.",
)
@has_permissions_decorator(["parking.view_parkingrecord"])
def get_records(
    request: HttpRequest, filters: FilterRecordSchema = Query(...)
) -> tuple[int, list[RecordSchema] | GenericMensageSchema]:
    """Retorna todos os Registros com base nos filtros.

    Verifica se o usuário tem a permissão `parking.view_parkingrecord`.
    Se tiver, busca os `ParkingRecords` e filtra eles com base em `filters`
    (a lista pode ser retornada vazia) e retorna
    `(200, list[RecordSchema])`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`.

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        filters (FilterRecordSchema): campos para filtrar os ParkingRecords.

    Returns:
        tuple[int, list[RecordSchema | GenericMensageSchema]: tupla contendo
        o status HTTP e o corpo da resposta.

    Responses:
        200: Lista de ParkingRecord.
        403: Usuário não autorizado.
        500: Erro interno do servidor.

    """
    try:
        records = ParkingRecord.objects.for_owner(user=request.user)

        if filters:
            records = filters.filter(records)

        return 200, records

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@records_router.get(
    path="/{id}",
    response={
        200: RecordSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que devolve o Registro com id igual ao passado na url.",
)
@has_permissions_decorator(["parking.view_parkingrecord"])
def get_record(
    request: HttpRequest, id: int
) -> tuple[int, RecordSchema | GenericMensageSchema]:
    """Retorna o Registro com id igual ao da url.

    Verifica se o usuário tem a permissão `parking.view_parkingrecord`.
    Se tiver, busca o `ParkingRecord` com o mesmo id da url e retorna
    `(200, RecordSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `ParkingRecord`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do Registro.

    Returns:
        tuple[int, RecordSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Registro com o mesmo id da url.
        403: Usuário não autorizado.
        404: Registro não encontrado.
        500: Erro interno do servidor.

    """
    try:
        record = ParkingRecord.objects.for_owner(user=request.user).get(id=id)

        return 200, record

    except ParkingRecord.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Registro")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()


@records_router.patch(
    path="/{id}",
    response={
        200: RecordSchema,
        403: GenericMensageSchema,
        404: GenericMensageSchema,
        500: GenericMensageSchema,
    },
    summary="Rota que atualiza parcialmente o registro.",
)
@has_permissions_decorator(["parking.change_parkingrecord"])
def patch_record(
    request: HttpRequest, id: int, payload: PatchRecordSchema
) -> tuple[int, RecordSchema | GenericMensageSchema]:
    """Atualiza o Registro com id igual ao da url.

    Verifica se o usuário tem a permissão `parking.change_parkingrecord`.
    Se tiver, busca o `ParkingRecord` com o mesmo id da url e o atualiza com
    base nos campos passados no payload e retorna
    `(200, RecordSchema)`. Se o usuário não tiver permissão, retorna
    `(403, GenericMensageSchema)`. Se não encontrar o `ParkingRecord`, retorna
    `(404, GenericMensageSchema)`. Em caso de erro interno, retorna
    `(500, GenericMensageSchema)`

    Args:
        request (HttpRequest): requisição HTTP com o usuário autenticado.
        id (int): id do ParkingRecord.
        payload (PatchRecordSchema): dados dos campos a serem atualizados.

    Returns:
        tuple[int, RecordSchema | GenericMensageSchema]: tupla contendo o
        status HTTP e o corpo da resposta.

    Responses:
        200: Registro atualizado.
        403: Usuário não autorizado.
        404: Registro não encontrado.
        500: Erro interno do servidor.

    """
    try:
        record = ParkingRecord.objects.get(id=id)

        update_service(payload, record)

        record.save()

        return 200, record

    except ParkingRecord.DoesNotExist:
        return 404, GenericMensageSchema.not_found_menssage("Registro")

    except Exception:
        return 500, GenericMensageSchema.internal_erro_menssage()
