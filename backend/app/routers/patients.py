import random
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Patient, User, HealthRecord, PredictionLog
from ..schemas import PatientCreate, PatientResponse
from ..auth import get_current_user

router = APIRouter(prefix="/patients", tags=["Patients"])

def generate_patient_code(db: Session) -> str:
    count = db.query(Patient).count() + 1
    return f"DV-{count:04d}"

@router.get("/", response_model=List[PatientResponse])
def list_patients(
    search: Optional[str] = None,
    risk_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Patient)
    if search:
        query = query.filter(
            (Patient.full_name.ilike(f"%{search}%")) |
            (Patient.patient_code.ilike(f"%{search}%"))
        )
    patients = query.order_by(Patient.id.desc()).all()
    
    results = []
    for p in patients:
        # Get latest vitals
        latest_record = db.query(HealthRecord).filter(HealthRecord.patient_id == p.id).order_by(HealthRecord.recorded_at.desc()).first()
        vitals_dict = None
        if latest_record:
            vitals_dict = {
                "recorded_at": latest_record.recorded_at,
                "systolic_bp": latest_record.systolic_bp,
                "diastolic_bp": latest_record.diastolic_bp,
                "fasting_glucose": latest_record.fasting_glucose,
                "bmi": latest_record.bmi,
                "total_cholesterol": latest_record.total_cholesterol
            }
        
        # Get latest risk predictions
        latest_preds = db.query(PredictionLog).filter(PredictionLog.patient_id == p.id).order_by(PredictionLog.created_at.desc()).limit(3).all()
        risks_dict = {}
        for pred in latest_preds:
            risks_dict[pred.disease_type.lower()] = {
                "score": pred.risk_score,
                "level": pred.risk_level
            }
        
        # Optional risk filter
        if risk_filter and risk_filter.upper() != "ALL":
            has_matching_risk = any(r["level"] == risk_filter.upper() for r in risks_dict.values())
            if not has_matching_risk:
                continue

        p_dict = {
            "id": p.id,
            "patient_code": p.patient_code,
            "full_name": p.full_name,
            "age": p.age,
            "gender": p.gender,
            "blood_group": p.blood_group,
            "contact_phone": p.contact_phone,
            "contact_email": p.contact_email,
            "medical_history": p.medical_history,
            "created_at": p.created_at,
            "latest_vitals": vitals_dict,
            "latest_risks": risks_dict
        }
        results.append(p_dict)

    return results

@router.post("/", response_model=PatientResponse)
def create_patient(
    patient_in: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    code = patient_in.patient_code or generate_patient_code(db)
    patient = Patient(
        patient_code=code,
        full_name=patient_in.full_name,
        age=patient_in.age,
        gender=patient_in.gender,
        blood_group=patient_in.blood_group,
        contact_phone=patient_in.contact_phone,
        contact_email=patient_in.contact_email,
        medical_history=patient_in.medical_history,
        assigned_doctor_id=current_user.id
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    latest_record = db.query(HealthRecord).filter(HealthRecord.patient_id == patient.id).order_by(HealthRecord.recorded_at.desc()).first()
    vitals_dict = None
    if latest_record:
        vitals_dict = {
            "recorded_at": latest_record.recorded_at,
            "systolic_bp": latest_record.systolic_bp,
            "diastolic_bp": latest_record.diastolic_bp,
            "fasting_glucose": latest_record.fasting_glucose,
            "bmi": latest_record.bmi,
            "total_cholesterol": latest_record.total_cholesterol
        }

    latest_preds = db.query(PredictionLog).filter(PredictionLog.patient_id == patient.id).order_by(PredictionLog.created_at.desc()).limit(3).all()
    risks_dict = {pred.disease_type.lower(): {"score": pred.risk_score, "level": pred.risk_level} for pred in latest_preds}

    return {
        "id": patient.id,
        "patient_code": patient.patient_code,
        "full_name": patient.full_name,
        "age": patient.age,
        "gender": patient.gender,
        "blood_group": patient.blood_group,
        "contact_phone": patient.contact_phone,
        "contact_email": patient.contact_email,
        "medical_history": patient.medical_history,
        "created_at": patient.created_at,
        "latest_vitals": vitals_dict,
        "latest_risks": risks_dict
    }

