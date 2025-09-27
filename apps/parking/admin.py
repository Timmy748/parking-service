"""Admin da app parking."""

from typing import Any

from django.contrib import admin
from django.db.models import ForeignKey
from django.http import HttpRequest

from .models import ParkingRecord, ParkingSpot


@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    """Admin para a model ParkingSpot.

    Exibe os campos `spot_number` e `is_occupied` na listagem.
    Permite busca pelo campo `spot_number`. Permite filtro pelo campo
    `is_occupied`.

    """

    list_display = ["spot_number", "is_occupied"]
    search_fields = ["spot_number"]
    list_filter = ["is_occupied"]


@admin.register(ParkingRecord)
class ParkingRecordAdmin(admin.ModelAdmin):
    """Admin para a model ParkingRecord.

    Exibe os campos `vehicle`, `parking_spot`, `entry_time` e `exit_time`
    na listagem. Permite busca pelos campos `vehicle__license_plate` e
    `parking_spot__spot_number`. No formulário de adição, o campo
    `parking_spot` exibe apenas vagas que não estão ocupadas.

    """

    list_display = ["vehicle", "parking_spot", "entry_time", "exit_time"]
    search_fields = ["vehicle__license_plate", "parking_spot__spot_number"]

    def formfield_for_foreignkey(
        self, db_field: ForeignKey, request: HttpRequest, **kwargs: Any
    ) -> Any:
        """Personaliza o queryset do campo parking_spot no formulário.

        Se o campo for parking_spot e a página não for de alteração, filtra o
        queryset para exibir apenas vagas que não estão ocupadas.

        Args:
            db_field (ForeignKey): O campo de chave estrangeira.
            request (HttpRequest): A requisição HTTP.
            **kwargs (Any): Argumentos adicionais.

        Returns:
            Any: O campo de formulário personalizado.

        """
        is_parking_spot = db_field.name == "parking_spot"
        is_not_change_page = not request.resolver_match.url_name.endswith(
            "change"
        )

        if is_parking_spot and is_not_change_page:
            kwargs["queryset"] = ParkingSpot.objects.filter(is_occupied=False)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
