"""Testes para o GenericMessageSchema."""

from django.test import TestCase

from utils.schemas import GenericMensageSchema


class GenericMensageSchemaTest(TestCase):
    """Testa os métodos de GenericMessageSchema.

    Esta classe verifica se os métodos de mensagem genérica geram o
    texto esperado para diferentes situações, para garantir a consistência
    e correção das mensagens retornadas pela API.

    """

    def test_deleted_menssage_with_customer(self) -> None:
        """Verifica se deleted_message cria a mensagem certa para uma model.

        Testa se a mensagem gerada corresponde ao texto esperado quando
        informamos a model 'customer'.
        """
        schema = GenericMensageSchema.deleted_menssage("customer")

        self.assertEqual("Customer deletado(a) com sucesso", schema.menssage)

    def test_unauthorized_menssage(self) -> None:
        """Verifica se unauthorized_message cria a mensagem certa.

        Testa se a mensagem gerada indica corretamente que o usuário não
        tem permissão para acessar o recurso.
        """
        schema = GenericMensageSchema.unauthorized_menssage()

        self.assertEqual(
            "Apenas administaradores tem essa função", schema.menssage
        )

    def test_internal_erro_menssage(self) -> None:
        """Verifica se internal_error_message retorna a mensagem certa.

        Testa se a mensagem gerada indica corretamente que ocorreu um
        erro interno no servidor.
        """
        schema = GenericMensageSchema.internal_erro_menssage()

        self.assertEqual("Erro interno no servidor", schema.menssage)

    def test_not_found_menssage(self) -> None:
        """Verifica se not_found_menssage cria a mensagem certa para uma model.

        Testa se a mensagem gerada corresponde ao texto esperado quando
        informamos a model 'customer' que não foi encontrada.
        """
        schema = GenericMensageSchema.not_found_menssage("customer")

        self.assertEqual("Customer não encontrado(a)", schema.menssage)
