from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController

from apps.customers.api import customer_router
from apps.parking.api import records_router, spots_router
from apps.vehicles.api import (
    vehicle_brands_router,
    vehicle_colors_router,
    vehicle_models_router,
    vehicle_types_router,
    vehicles_router,
)

api = NinjaExtraAPI(
    title="Api de Estacionamento",
    description="Api feita baseada nas quatro lives do canal PycodeBR.",
    version="1.0.0",
    auth=JWTAuth(),
)

api.register_controllers(
    NinjaJWTDefaultController,
)


api.add_router("/customers", customer_router)

api.add_router("/records", records_router)
api.add_router("/sposts", spots_router)

api.add_router("/vehicles", vehicles_router)
api.add_router("/vehicles/types", vehicle_types_router)
api.add_router("/vehicles/brands", vehicle_brands_router)
api.add_router("/vehicles/models", vehicle_models_router)
api.add_router("/vehicles/colors", vehicle_colors_router)

