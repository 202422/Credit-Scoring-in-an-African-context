import traceback
from fastapi import APIRouter, HTTPException
from models.schema import CreditRiskRequest, CreditRiskResponse
from services.prediction_process import predict_process

router = APIRouter()

@router.post("/predict", response_model=CreditRiskResponse)
def predict(data: CreditRiskRequest):
    try:
        data_dict = data.dict()
        return predict_process(data=data_dict)
    except Exception as e:
        print("=== ERROR ===")
        traceback.print_exc()   # affiche l’erreur complète dans la console
        raise HTTPException(status_code=500, detail=str(e) or "Unknown error")
