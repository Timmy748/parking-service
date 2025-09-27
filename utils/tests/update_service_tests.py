"""Testes para o serviço de atualização genérico."""

from django.test import TestCase

from apps.customers.models import Customer
from apps.customers.schemas import PatchCustomerSchema
from utils.services import update_service


class UpdateServiceTestCase(TestCase):
    """Testa o serviço de atualização genérico.

    Esta classe verifica se o serviço de atualização funciona corretamente
    para diferentes cenários, garantindo que os dados sejam atualizados e
    persistidos conforme esperado.
    """

    def setUp(self) -> None:
        self.customer = Customer.objects.create(name="naruto")
        self.payload = PatchCustomerSchema(cpf="11122233344", name="sasuke")

    def test_update_with_save_true(self) -> None:
        """Atualiza e persiste no banco quando save=True.

        Verifica se o serviço aplica as alterações ao objeto e
        persiste as mudanças no banco de dados quando o parâmetro
        `save` é definido como `True`.

        """
        update_service(self.payload, self.customer, save=True)

        self.customer.refresh_from_db()

        self.assertEqual("sasuke", self.customer.name)
        self.assertEqual("11122233344", self.customer.cpf)

    def test_update_with_save_false(self) -> None:
        """Atualiza apenas em memória quando save=False.

        Verifica se o serviço aplica as alterações ao objeto em
        memória, mas não persiste no banco de dados quando o
        parâmetro ``save`` é definido como ``False``.
        """
        update_service(self.payload, self.customer, save=False)

        self.assertEqual("sasuke", self.customer.name)
        self.assertEqual("11122233344", self.customer.cpf)

        customer_from_db = Customer.objects.get(id=self.customer.id)
        self.assertEqual("naruto", customer_from_db.name)
        self.assertEqual(None, customer_from_db.cpf)



