"""Funções ultilitárias para atualizar instâncias de uma Model qualquer."""

from typing import Any

from django.db.models import Model
from ninja import Schema


def update_service[T: Model](
    data: Schema | dict[str, Any], instance: T, save: bool = True
) -> T:
    """Atualiza os atributos de uma instância de uma model qualquer.

    Essa função transfomar o `payload` em um dict só com os campos
    fornecidos e atualiza a instância com base nesse dict.

    Args:
        data (Schema | dict[str, Any]): Schema ou Dict de entrada contendo
        os novos valores.
        instance (Model): Instância de uma Model a ser atualizada.
        save (bool): Indica se deve salvar ou não as mudanças.

    Returns:
        Model: A instância do modelo atualizada (mas **não salva** por padrão;
        é necessário chamar `instance.save()`explicitamente após o uso caso
        não passe `save` = True).

    """
    if not isinstance(data, dict):
        data = data.dict(exclude_unset=True)

    for field, value in data.items():
        setattr(instance, field, value)

    if save:
        instance.save()

    return instance
