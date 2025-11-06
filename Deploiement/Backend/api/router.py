from fastapi import APIRouter
from api.endpoints import prediction

router = APIRouter()
router.include_router(prediction.router, prefix="/api", tags=["Credit Scoring"])