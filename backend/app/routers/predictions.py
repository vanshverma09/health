import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Patient, PredictionLog, HealthRecord, User
from ..schemas import (
    DiseaseRiskPredictionRequest,
    MultiDiseaseRiskResponse,
    SingleDiseaseRiskResult,
    WhatIfRequest,
    WhatIfResponse
)
from ..auth import get_current_user
from ..ml_engine.predictor import predictor

router = APIRouter(prefix="/predict", tags=["Disease Risk Predictions"])

@router.post("/disease-risk", response_model=MultiDiseaseRiskResponse)
def predict_disease_risk(
    req: DiseaseRiskPredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data_dict = req.dict()
    prediction_output = predictor.predict(data_dict)
    
    # If patient_id is provided, save predictions to database
    if req.patient_id:
        patient = db.query(Patient).filter(Patient.id == req.patient_id).first()
        if patient:
            # Find latest health record if any
            latest_rec = db.query(HealthRecord).filter(
                HealthRecord.patient_id == patient.id
            ).order_by(HealthRecord.recorded_at.desc()).first()

            for disease_key, risk_info in prediction_output["risks"].items():
                log_entry = PredictionLog(
                    patient_id=patient.id,
                    health_record_id=latest_rec.id if latest_rec else None,
                    disease_type=risk_info["disease_type"],
                    risk_score=risk_info["risk_score"],
                    risk_level=risk_info["risk_level"],
                    feature_contributions=risk_info["feature_contributions"],
                    clinical_recommendations=risk_info["clinical_recommendations"]
                )
                db.add(log_entry)
            db.commit()

    return {
        "timestamp": datetime.datetime.utcnow(),
        "overall_health_score": prediction_output["overall_health_score"],
        "risks": prediction_output["risks"]
    }

@router.post("/what-if", response_model=WhatIfResponse)
def simulate_what_if_lifestyle(
    req: WhatIfRequest,
    current_user: User = Depends(get_current_user)
):
    sim_output = predictor.simulate_what_if(
        baseline_data=req.baseline_data.dict(),
        modified_params=req.modified_params
    )
    return sim_output

@router.get("/history/{patient_id}")
def get_prediction_history(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logs = db.query(PredictionLog).filter(
        PredictionLog.patient_id == patient_id
    ).order_by(PredictionLog.created_at.desc()).limit(15).all()
    
    return [
        {
            "id": log.id,
            "disease_type": log.disease_type,
            "risk_score": log.risk_score,
            "risk_percentage": round(log.risk_score * 100, 1),
            "risk_level": log.risk_level,
            "feature_contributions": log.feature_contributions,
            "clinical_recommendations": log.clinical_recommendations,
            "created_at": log.created_at
        }
        for log in logs
    ]

