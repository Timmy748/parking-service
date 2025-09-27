"""Classe de respostas genéricas para rotas da aplicação."""

from ninja import Schema


class GenericMensageSchema(Schema):
    """Schema para mensagens genéricas de resposta.

    Usado para retornar mensagens padrão em respostas de API. Inclui
    métodos de classe para criar mensagens comuns, como confirmação de
    deleção, mensagens de erro e notificações de permissão.

    """

    menssage: str

    @classmethod
    def deleted_menssage(cls, model: str) -> "GenericMensageSchema":
        """Mensagem informando que uma instância foi deletada com sucesso.

        Args:
            model (str): Nome da model deletada.

        Returns:
            GenericMensageSchema: GenericMensageSchema com
            menssage igual f"{model.title()} deletado(a) com sucesso"

        """
        return cls(
            menssage=f"{model.title()} deletado(a) com sucesso",
        )

    @classmethod
    def unauthorized_menssage(cls) -> "GenericMensageSchema":
        """Mensagem informando que o usuário não tem permissão para acessar.

        Returns:
            GenericMensageSchema: GenericMensageSchema com
            menssage igual "Apenas administaradores tem essa função"

        """
        return cls(
            menssage="Apenas administaradores tem essa função",
        )

    @classmethod
    def internal_erro_menssage(cls) -> "GenericMensageSchema":
        """Mensagem informando um erro interno do servidor.

        Returns:
            GenericMensageSchema: GenericMensageSchema com
            menssage igual "Erro interno no servidor"

        """
        return cls(
            menssage="Erro interno no servidor",
        )

    @classmethod
    def not_found_menssage(cls, model: str) -> "GenericMensageSchema":
        """Mensagem informando que um recurso não foi encontrado.

        Args:
            model (str): Nome da model não encontrada.

        Returns:
            GenericMensageSchema: GenericMensageSchema com
            menssage igual f"{model.title()} não encontrado(a)"

        """
        return cls(
            menssage=f"{model.title()} não encontrado(a)",
        )
