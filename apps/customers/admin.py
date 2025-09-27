"""Admin da app customers."""

from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin para a model Customer.

    Exibe os campos `name`, `cpf`, `phone` e `created_at` na listagem.
    Permite busca pelos campos `name`, `cpf` e `phone`.

    """

    list_display = ["name", "cpf", "phone", "created_at"]
    search_fields = ["name", "cpf", "phone"]
