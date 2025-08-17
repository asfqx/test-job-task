from .get_bank_from_api import router as router_get_bank_api
from .get_bank_from_bintable import router as router_get_bank_bintable
from fastapi import APIRouter


router = APIRouter(prefix="/api", tags=["api"])
router.include_router(router_get_bank_api)
router.include_router(router_get_bank_bintable)
