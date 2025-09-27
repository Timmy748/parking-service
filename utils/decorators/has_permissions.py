"""Decorator que verifica permissão do usuário para rotas."""

from collections.abc import Callable, Iterable
from functools import wraps

from django.contrib.auth.models import User
from django.http import HttpRequest

from ..schemas import GenericMensageSchema
from ..services import has_permissions


def has_permissions_decorator[**P, R](
    permissions: Iterable[str],
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorador para verificar se o usuário acesso ao recurso.

    Verifica se o `user` vindo da `request` já autentificada tem as
    permissões necessárias para acessar a rota.

    Args:
        permissions (Iterable[str]): Interable com permissões a serem checadas.

    Returns:
        Callable[[Callable[P, R]], Callable[P, R]]: função que verifica se o
        `user` tem permissão antes de usar a função padrão da rota.

    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def inner(
            request: HttpRequest, *args: P.args, **kwargs: P.kwargs
        ) -> R | tuple[int | GenericMensageSchema]:
            user: User | None = getattr(request, "user", None)

            if user is None or not has_permissions(user, permissions):
                return 403, GenericMensageSchema.unauthorized_menssage()

            return func(request, *args, **kwargs)

        return inner

    return decorator
