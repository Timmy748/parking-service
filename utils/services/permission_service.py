"""Funções ultilitárias para verificar permissões do usuários."""

from collections.abc import Iterable

from django.contrib.auth.models import User


def is_internal_user(user: User) -> bool:
    """Verifica se o `user` é admin ou parte da staff.

    Args:
        user (User): instancia de usuário a ser verificado.

    Returns:
        bool: representa se é ou não admin ou staff.

    """
    return user.is_superuser or user.is_staff


def has_permissions(
    user: User, permissions: Iterable[str] | None = None
) -> bool:
    """Verifica se o usuário possui as permissões necessárias.

    Essa verificação retorna verdadeiro se o `user` tiver todas as permissões
    em `permissions`, ou se ele for um superusuário ou parte da equipe interna.

    Args:
        user (User): Instância de usuário a ser verificado.
        permissions (Iterable[str] | None): Iterável de permissões necessárias.

    Returns:
        bool: Verdadeiro se o usuário tiver permissão, falso caso contrário.

    """
    if permissions is None:
        return is_internal_user(user)

    return is_internal_user(user) or user.has_perms(permissions)
