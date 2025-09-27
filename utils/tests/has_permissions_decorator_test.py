"""Testes para o decorator de permissões."""

from django.contrib.auth.models import AnonymousUser, Permission, User
from django.http import HttpRequest
from django.test import TestCase

from utils.decorators import has_permissions_decorator
from utils.schemas import GenericMensageSchema


class HasPermissionsDecoratorTest(TestCase):
    """Testa o decorator has_permissions_decorator.

    Esta classe verifica o decorator retorna uma view qualquer
    corretamente após adicionar a verificação da service `has_permissions`.

    """

    def setUp(self) -> None:
        self.request: HttpRequest = HttpRequest()

    def test_returns_403_for_anonymous_user(self) -> None:
        """Testa se impede um usuário anonimo de acessar o recurso."""
        self.request.user = AnonymousUser()

        @has_permissions_decorator(["app.view_model"])
        def view(request):
            return "ok"

        result = view(self.request)

        self.assertIsInstance(result, tuple)
        status, msg = result
        self.assertEqual(403, status)
        self.assertEqual(GenericMensageSchema.unauthorized_menssage(), msg)

    def test_returns_403_for_user_without_permissions(self) -> None:
        """Testa se impede um usuário não autorizado de acessar o recurso."""
        self.request.user = User.objects.create_user(
            username="Naruto", password="123"
        )

        @has_permissions_decorator(["app.view_model"])
        def view(request):
            return "ok"

        result = view(self.request)

        self.assertIsInstance(result, tuple)
        status, msg = result
        self.assertEqual(403, status)
        self.assertEqual(GenericMensageSchema.unauthorized_menssage(), msg)

    def test_returns_403_for_user_with_permissions(self) -> None:
        """Testa se permite um usuário autorizado acessar o recurso."""
        user = User.objects.create_user(username="Naruto", password="123")
        permission = Permission.objects.get(codename="add_user")
        user.user_permissions.add(permission)

        self.request.user = user

        @has_permissions_decorator(["auth.add_user"])
        def view(request):
            return "ok"

        result = view(self.request)

        self.assertEqual("ok", result)
