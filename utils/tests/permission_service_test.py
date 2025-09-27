"""Testes para o PermissionService."""

from django.contrib.auth.models import Permission, User
from django.test import TestCase

from utils.services import has_permissions, is_internal_user


class PermissionServiceTest(TestCase):
    """Testa as funções de permission_service.

    Esta classe verifica se as funções de permissão funcionam corretamente
    para diferentes tipos de usuários, garantindo que as permissões sejam
    aplicadas conforme esperado.

    """

    def setUp(self) -> None:
        self.super_user = User.objects.create_superuser(
            username="super", email="test@gmail.com", password="123"
        )

        self.staff_user = User.objects.create_user(
            username="staff",
            email="test@gmail.com",
            password="123",
            is_staff=True,
        )

        self.user = User.objects.create_user(
            username="user", email="test@gmail.com", password="123"
        )

        self.permission = "auth.add_user"

    def test_is_internal_user_with_common_user(self) -> None:
        """Testa se retorna False para um usuário comum do sistema."""
        result: bool = is_internal_user(self.user)

        self.assertEqual(False, result)

    def test_is_internal_user_with_staff_user(self) -> None:
        """Testa se retorna True para um membro da staff do sistema."""
        result: bool = is_internal_user(self.staff_user)

        self.assertEqual(True, result)

    def test_is_internal_user_with_super_user(self) -> None:
        """Testa se retorna True para um super usuário do sistema."""
        result: bool = is_internal_user(self.super_user)

        self.assertEqual(True, result)

    def test_has_permission_with_super_user(self) -> None:
        """Testa se retorna True para um super usuário do sistema."""
        result: bool = has_permissions(self.super_user)

        self.assertEqual(True, result)

    def test_has_permission_with_staff_user(self) -> None:
        """Testa se retorna True para um membro do staff do sistema."""
        result: bool = has_permissions(self.staff_user)

        self.assertEqual(True, result)

    def test_has_permission_with_user_without_permission(self) -> None:
        """Testa se retorna False para um usuário do sistema sem permissão."""
        result: bool = has_permissions(self.user, [self.permission])

        self.assertEqual(False, result)

    def test_has_permission_with_user_with_permission(self) -> None:
        """Testa se retorna True para um usuário do sistema com permissão."""
        self.user.user_permissions.add(
            Permission.objects.get(codename="add_user")
        )

        result: bool = has_permissions(self.user, [self.permission])

        self.assertEqual(True, result)
