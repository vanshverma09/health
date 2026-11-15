import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(120), nullable=False)
    role = Column(String(20), default="doctor") # "doctor", "patient", "admin"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    patients_created = relationship("Patient", back_populates="doctor")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_code = Column(String(30), unique=True, index=True, nullable=False)
    full_name = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False) # "Male", "Female", "Other"
    blood_group = Column(String(5), nullable=True) # e.g. "O+", "A+"
    contact_phone = Column(String(20), nullable=True)
    contact_email = Column(String(120), nullable=True)
    assigned_doctor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    medical_history = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    doctor = relationship("User", back_populates="patients_created")
    health_records = relationship("HealthRecord", back_populates="patient", cascade="all, delete-orphan", order_by="desc(HealthRecord.recorded_at)")
    prediction_logs = relationship("PredictionLog", back_populates="patient", cascade="all, delete-orphan", order_by="desc(PredictionLog.created_at)")

class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Core Vitals & Biomarkers
    systolic_bp = Column(Integer, nullable=False) # mmHg (e.g. 120)
    diastolic_bp = Column(Integer, nullable=False) # mmHg (e.g. 80)
    heart_rate = Column(Integer, nullable=True) # bpm (e.g. 72)
    fasting_glucose = Column(Float, nullable=False) # mg/dL (e.g. 95)
    hba1c = Column(Float, nullable=True) # % (e.g. 5.6)
    total_cholesterol = Column(Float, nullable=False) # mg/dL (e.g. 190)
    hdl_cholesterol = Column(Float, nullable=True) # mg/dL (e.g. 50)
    ldl_cholesterol = Column(Float, nullable=True) # mg/dL (e.g. 110)
    bmi = Column(Float, nullable=False) # kg/m² (e.g. 24.5)
    
    # Lifestyle factors
    smoking_status = Column(Boolean, default=False)
    alcohol_consumption = Column(Boolean, default=False)
    physical_activity_hours = Column(Float, default=3.0) # hours per week
    notes = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="health_records")
    predictions = relationship("PredictionLog", back_populates="health_record", cascade="all, delete-orphan")

class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    health_record_id = Column(Integer, ForeignKey("health_records.id"), nullable=True)
    
    disease_type = Column(String(50), nullable=False) # HEART_DISEASE, DIABETES, STROKE
    risk_score = Column(Float, nullable=False) # 0.0 to 1.0 (e.g. 0.78 = 78%)
    risk_level = Column(String(20), nullable=False) # LOW, MODERATE, HIGH, CRITICAL
    
    # Explainable AI metrics (contributions of each feature to the risk)
    feature_contributions = Column(JSON, nullable=True) # {"glucose": +0.28, "bmi": +0.15, ...}
    clinical_recommendations = Column(JSON, nullable=True) # ["Reduce daily sodium", "Target BMI < 25"]
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    patient = relationship("Patient", back_populates="prediction_logs")
    health_record = relationship("HealthRecord", back_populates="predictions")

