import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field

# ----------------- Auth & User Schemas -----------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str
    role: str = "doctor"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# ----------------- Patient Schemas -----------------
class PatientBase(BaseModel):
    patient_code: Optional[str] = None
    full_name: str
    age: int = Field(..., ge=1, le=120)
    gender: str = Field(..., pattern="^(Male|Female|Other)$")
    blood_group: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    medical_history: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    created_at: datetime.datetime
    latest_vitals: Optional[Dict[str, Any]] = None
    latest_risks: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

# ----------------- Health Record & Vitals Schemas -----------------
class HealthRecordCreate(BaseModel):
    patient_id: int
    systolic_bp: int = Field(..., ge=60, le=260, description="Systolic Blood Pressure (mmHg)")
    diastolic_bp: int = Field(..., ge=40, le=160, description="Diastolic Blood Pressure (mmHg)")
    heart_rate: Optional[int] = Field(72, ge=40, le=220)
    fasting_glucose: float = Field(..., ge=40, le=500, description="Fasting Glucose (mg/dL)")
    hba1c: Optional[float] = Field(None, ge=3.0, le=20.0, description="HbA1c percentage")
    total_cholesterol: float = Field(..., ge=80, le=600, description="Total Cholesterol (mg/dL)")
    hdl_cholesterol: Optional[float] = Field(None, ge=10, le=150)
    ldl_cholesterol: Optional[float] = Field(None, ge=20, le=400)
    bmi: float = Field(..., ge=10.0, le=70.0, description="Body Mass Index (kg/m²)")
    smoking_status: bool = False
    alcohol_consumption: bool = False
    physical_activity_hours: float = Field(3.0, ge=0.0, le=40.0)
    notes: Optional[str] = None

class HealthRecordResponse(HealthRecordCreate):
    id: int
    recorded_at: datetime.datetime

    class Config:
        from_attributes = True

# ----------------- Prediction & Explainability Schemas -----------------
class DiseaseRiskPredictionRequest(BaseModel):
    patient_id: Optional[int] = None
    age: int
    gender: str # "Male", "Female", "Other"
    systolic_bp: int
    diastolic_bp: int
    heart_rate: Optional[int] = 72
    fasting_glucose: float
    total_cholesterol: float
    bmi: float
    smoking_status: bool = False
    physical_activity_hours: float = 3.0

class SingleDiseaseRiskResult(BaseModel):
    disease_type: str
    risk_score: float # 0.0 - 1.0
    risk_percentage: float # 0 - 100%
    risk_level: str # LOW, MODERATE, HIGH, CRITICAL
    color: str # hex color code for UI
    feature_contributions: List[Dict[str, Any]]
    clinical_recommendations: List[str]

class MultiDiseaseRiskResponse(BaseModel):
    timestamp: datetime.datetime
    overall_health_score: float # 0 - 100
    risks: Dict[str, SingleDiseaseRiskResult]

class WhatIfRequest(BaseModel):
    baseline_data: DiseaseRiskPredictionRequest
    modified_params: Dict[str, Any]

class WhatIfResponse(BaseModel):
    baseline_risks: Dict[str, SingleDiseaseRiskResult]
    simulated_risks: Dict[str, SingleDiseaseRiskResult]
    risk_delta: Dict[str, float] # negative means risk improved

