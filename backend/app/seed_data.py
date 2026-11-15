import datetime
import random
from .database import SessionLocal, engine, Base
from .models import User, Patient, HealthRecord, PredictionLog
from .auth import get_password_hash
from .ml_engine.predictor import predictor
from .ml_engine.trainer import train_and_export_models, MODELS_DIR
import os

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Ensure models are trained
    required_models = ["heart_disease_model.joblib", "diabetes_model.joblib", "stroke_model.joblib"]
    if not all(os.path.exists(os.path.join(MODELS_DIR, m)) for m in required_models):
        print("Training models before seeding...")
        train_and_export_models()

    # Check if doctor already exists
    doc = db.query(User).filter(User.email == "doctor@datavision.com").first()
    if not doc:
        doc = User(
            email="doctor@datavision.com",
            hashed_password=get_password_hash("password123"),
            full_name="Dr. Eleanor Vance, MD",
            role="doctor"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        print("Created default doctor account: doctor@datavision.com / password123")

    if db.query(Patient).count() > 0:
        print("Patients already seeded.")
        db.close()
        return

    # Sample realistic patient profiles
    patient_templates = [
        {"name": "Arthur Pendelton", "age": 62, "gender": "Male", "blood": "O+", "phone": "+1-555-0192", "history": "Hypertension stage 1, former smoker."},
        {"name": "Sarah Jenkins", "age": 45, "gender": "Female", "blood": "A+", "phone": "+1-555-0143", "history": "Gestational diabetes history, sedentary office worker."},
        {"name": "Carlos Rodriguez", "age": 58, "gender": "Male", "blood": "B-", "phone": "+1-555-0188", "history": "Hyperlipidemia, familial history of early coronary artery disease."},
        {"name": "Priya Sharma", "age": 34, "gender": "Female", "blood": "O-", "phone": "+1-555-0177", "history": "Annual physical checkup, active runner, asymptomatic."},
        {"name": "David Kim", "age": 71, "gender": "Male", "blood": "AB+", "phone": "+1-555-0164", "history": "Previous transient ischemic attack (TIA), high systolic blood pressure."},
        {"name": "Elena Rostova", "age": 51, "gender": "Female", "blood": "A-", "phone": "+1-555-0129", "history": "Mild obesity, early signs of metabolic syndrome."},
        {"name": "Marcus Aurelius Reed", "age": 40, "gender": "Male", "blood": "O+", "phone": "+1-555-0111", "history": "Borderline elevated LDL cholesterol, high stress lifestyle."},
        {"name": "Amina Al-Mansoor", "age": 28, "gender": "Female", "blood": "B+", "phone": "+1-555-0155", "history": "Baseline healthy vitals, prenatal consultation."}
    ]

    print("Seeding demo patients and historical longitudinal health records...")
    now = datetime.datetime.utcnow()

    for idx, p_info in enumerate(patient_templates):
        patient = Patient(
            patient_code=f"DV-10{idx+1:02d}",
            full_name=p_info["name"],
            age=p_info["age"],
            gender=p_info["gender"],
            blood_group=p_info["blood"],
            contact_phone=p_info["phone"],
            contact_email=f"patient_{idx+1}@example.com",
            medical_history=p_info["history"],
            assigned_doctor_id=doc.id
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)

        # Generate 4 chronological visits over the past 9 months for timeline charts
        base_sbp = 145 if "Hyper" in p_info["history"] or patient.age > 60 else (118 if patient.age < 35 else 128)
        base_glucose = 135 if "diabetes" in p_info["history"].lower() else 92
        base_bmi = 31.0 if "obesity" in p_info["history"].lower() else (24.0 if patient.age < 35 else 27.2)
        base_chol = 230 if "lipidemia" in p_info["history"].lower() or "cholesterol" in p_info["history"].lower() else 185
        is_smoker = True if "smoker" in p_info["history"].lower() else False

        for visit_idx in range(4):
            visit_date = now - datetime.timedelta(days=(3 - visit_idx) * 75)
            # Add slight realistic drift/fluctuation
            v_sbp = int(base_sbp + random.randint(-6, 6) - (visit_idx * 2))
            v_dbp = int(v_sbp * 0.65 + random.randint(-4, 4))
            v_glucose = round(base_glucose + random.uniform(-8, 8) - (visit_idx * 1.5), 1)
            v_bmi = round(base_bmi + random.uniform(-0.5, 0.5) - (visit_idx * 0.2), 1)
            v_chol = round(base_chol + random.uniform(-10, 10), 1)

            record = HealthRecord(
                patient_id=patient.id,
                recorded_at=visit_date,
                systolic_bp=v_sbp,
                diastolic_bp=v_dbp,
                heart_rate=random.randint(68, 82),
                fasting_glucose=v_glucose,
                hba1c=round(5.4 + (v_glucose - 90) * 0.03, 1),
                total_cholesterol=v_chol,
                hdl_cholesterol=round(random.uniform(42, 60), 1),
                ldl_cholesterol=round(v_chol - 50, 1),
                bmi=v_bmi,
                smoking_status=is_smoker,
                alcohol_consumption=random.choice([True, False]),
                physical_activity_hours=round(random.uniform(1.5, 5.0), 1),
                notes=f"Clinical follow-up consultation {visit_idx+1}."
            )
            db.add(record)
            db.commit()
            db.refresh(record)

            # For the most recent visit, compute and store ML predictions
            if visit_idx == 3:
                pred_input = {
                    "age": patient.age,
                    "gender": patient.gender,
                    "systolic_bp": record.systolic_bp,
                    "diastolic_bp": record.diastolic_bp,
                    "heart_rate": record.heart_rate,
                    "fasting_glucose": record.fasting_glucose,
                    "total_cholesterol": record.total_cholesterol,
                    "bmi": record.bmi,
                    "smoking_status": record.smoking_status,
                    "physical_activity_hours": record.physical_activity_hours
                }
                pred_output = predictor.predict(pred_input)
                for d_key, r_info in pred_output["risks"].items():
                    p_log = PredictionLog(
                        patient_id=patient.id,
                        health_record_id=record.id,
                        disease_type=r_info["disease_type"],
                        risk_score=r_info["risk_score"],
                        risk_level=r_info["risk_level"],
                        feature_contributions=r_info["feature_contributions"],
                        clinical_recommendations=r_info["clinical_recommendations"],
                        created_at=visit_date
                    )
                    db.add(p_log)
                db.commit()

    print("Seed complete! 8 demo patients with full historical biomarker timelines and risk predictions created.")
    db.close()

if __name__ == "__main__":
    seed()

