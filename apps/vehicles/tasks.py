""""Tarefas relacionadas a veículos."""

from typing import Optional

from celery import shared_task
from playwright.sync_api import Browser, ElementHandle, Page, sync_playwright

from .models import Vehicle


@shared_task
def complete_vehicle_data(license_plate: str) -> None:
    """Completa os dados do veículo a partir da placa.

    Args:
        license_plate (str): Placa há ser procurada na página.

    """
    URL = "https://pycodebr.com.br/placas-carros/"

    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None

    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=True)
        page: Page = browser.new_page()
        page.goto(url=URL)
        page.wait_for_selector("table")
        xpath_expression: str = (
            f"//table//tr[td[1][normalize-space()='{license_plate}']]"
        )
        row: Optional[ElementHandle] = page.query_selector(xpath_expression)
        if row:
            cells: list[ElementHandle] = row.query_selector_all("td")
            brand = cells[1].inner_text().strip()
            model = cells[2].inner_text().strip()
            color = cells[3].inner_text().strip()

        browser.close()

    if brand and model and color:
        Vehicle.objects.filter(license_plate=license_plate).update(
            brand=brand, model=model, color=color
        )
