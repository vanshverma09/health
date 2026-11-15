from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Patient, HealthRecord, User
from ..schemas import HealthRecordCreate, HealthRecordResponse
from ..auth import get_current_user

router = APIRouter(prefix="/records", tags=["Health Records"])

@router.post("/", response_model=HealthRecordResponse)
def add_health_record(
    record_in: HealthRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = db.query(Patient).filter(Patient.id == record_in.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    record = HealthRecord(**record_in.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/timeline/{patient_id}", response_model=List[HealthRecordResponse])
def get_patient_timeline(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    records = db.query(HealthRecord).filter(
        HealthRecord.patient_id == patient_id
    ).order_by(HealthRecord.recorded_at.asc()).all()
    
    return records

