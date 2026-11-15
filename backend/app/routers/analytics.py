import io
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from ..database import get_db
from ..models import Patient, HealthRecord, PredictionLog, User
from ..auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics & Reporting"])

@router.get("/cohort")
def get_cohort_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_patients = db.query(Patient).count()
    total_records = db.query(HealthRecord).count()
    
    # Risk count
    high_risk_count = db.query(PredictionLog).filter(
        PredictionLog.risk_level.in_(["HIGH", "CRITICAL"])
    ).distinct(PredictionLog.patient_id).count()

    # Age groups
    age_groups = {
        "18-35": db.query(Patient).filter(Patient.age >= 18, Patient.age <= 35).count(),
        "36-50": db.query(Patient).filter(Patient.age >= 36, Patient.age <= 50).count(),
        "51-65": db.query(Patient).filter(Patient.age >= 51, Patient.age <= 65).count(),
        "65+": db.query(Patient).filter(Patient.age > 65).count(),
    }

    # 4 Disease prevalence metrics
    diseases = ["Heart Disease", "Diabetes", "Stroke", "Kidney"]
    prevalence = []
    for d in diseases:
        high_cnt = db.query(PredictionLog).filter(
            PredictionLog.disease_type.ilike(f"%{d}%"),
            PredictionLog.risk_level.in_(["HIGH", "CRITICAL"])
        ).count()
        label = "Kidney Disease (CKD)" if d == "Kidney" else d
        prevalence.append({
            "disease": label,
            "high_risk_cases": high_cnt,
            "prevalence_rate": round((high_cnt / max(total_patients, 1)) * 100, 1)
        })

    # Recent risk distribution
    risk_distribution = {
        "LOW": db.query(PredictionLog).filter(PredictionLog.risk_level == "LOW").count(),
        "MODERATE": db.query(PredictionLog).filter(PredictionLog.risk_level == "MODERATE").count(),
        "HIGH": db.query(PredictionLog).filter(PredictionLog.risk_level == "HIGH").count(),
        "CRITICAL": db.query(PredictionLog).filter(PredictionLog.risk_level == "CRITICAL").count(),
    }

    return {
        "total_patients": total_patients,
        "total_health_records": total_records,
        "high_risk_patients_count": high_risk_count,
        "age_groups": age_groups,
        "disease_prevalence": prevalence,
        "risk_distribution": risk_distribution
    }

@router.get("/report/pdf/{patient_id}")
def export_patient_pdf_report(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    latest_record = db.query(HealthRecord).filter(
        HealthRecord.patient_id == patient_id
    ).order_by(HealthRecord.recorded_at.desc()).first()

    latest_preds = db.query(PredictionLog).filter(
        PredictionLog.patient_id == patient_id
    ).order_by(PredictionLog.created_at.desc()).limit(4).all()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=14
    )
    heading_style = ParagraphStyle(
        'SectionHead',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=6
    )

    story.append(Paragraph("DATAVISION HEALTH CLINICAL OBSERVATORY", title_style))
    story.append(Paragraph(f"Multi-Disease Diagnostic Risk Profile | Report Generated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceAfter=14))

    patient_data = [
        [
            Paragraph("<b>Patient Name:</b> " + patient.full_name, styles['Normal']),
            Paragraph("<b>Patient ID:</b> " + patient.patient_code, styles['Normal']),
        ],
        [
            Paragraph(f"<b>Age / Sex:</b> {patient.age} yrs / {patient.gender}", styles['Normal']),
            Paragraph("<b>Blood Group:</b> " + (patient.blood_group or "N/A"), styles['Normal']),
        ],
        [
            Paragraph("<b>Contact:</b> " + (patient.contact_phone or "N/A"), styles['Normal']),
            Paragraph("<b>Evaluating Clinician:</b> Dr. " + current_user.full_name, styles['Normal']),
        ]
    ]
    t_patient = Table(patient_data, colWidths=[270, 270])
    t_patient.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_patient)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Latest Clinical Biomarkers", heading_style))
    if latest_record:
        vitals_table_data = [
            ["Biomarker / Metric", "Patient Value", "Standard Clinical Reference Range", "Status"],
            ["Blood Pressure (Systolic / Diastolic)", f"{latest_record.systolic_bp} / {latest_record.diastolic_bp} mmHg", "< 120 / 80 mmHg", "Elevated" if latest_record.systolic_bp >= 130 else "Optimal"],
            ["Fasting Blood Glucose", f"{latest_record.fasting_glucose} mg/dL", "70 - 99 mg/dL", "High" if latest_record.fasting_glucose >= 100 else "Normal"],
            ["Total Serum Cholesterol", f"{latest_record.total_cholesterol} mg/dL", "< 200 mg/dL", "High" if latest_record.total_cholesterol >= 200 else "Desirable"],
            ["Body Mass Index (BMI)", f"{latest_record.bmi:.1f} kg/m²", "18.5 - 24.9 kg/m²", "Overweight" if latest_record.bmi >= 25 else "Normal"],
            ["Tobacco Smoking Status", "Active Smoker" if latest_record.smoking_status else "Non-Smoker", "Non-Smoker", "High Risk" if latest_record.smoking_status else "Normal"],
            ["Weekly Physical Activity", f"{latest_record.physical_activity_hours} hrs/week", ">= 2.5 hrs/week", "Adequate" if latest_record.physical_activity_hours >= 2.5 else "Low Activity"]
        ]
        t_vitals = Table(vitals_table_data, colWidths=[180, 110, 150, 100])
        t_vitals.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_vitals)
    else:
        story.append(Paragraph("No vitals recorded yet.", styles['Normal']))

    story.append(Spacer(1, 12))

    story.append(Paragraph("Multi-Disease Prognostic Risk Assessment (4 Conditions)", heading_style))
    if latest_preds:
        pred_table_data = [["Disease Target", "Risk Score", "Risk Tier", "Primary Risk Contributors"]]
        for p in latest_preds:
            factors_str = ""
            if p.feature_contributions and isinstance(p.feature_contributions, list):
                top_factors = [f.get('label', '') for f in p.feature_contributions if f.get('is_risk_driver')]
                factors_str = ", ".join(top_factors[:3]) or "Biomarkers within normal threshold"

            pred_table_data.append([
                p.disease_type,
                f"{p.risk_score * 100:.1f}%",
                p.risk_level,
                factors_str
            ])

        t_preds = Table(pred_table_data, colWidths=[140, 80, 100, 220])
        t_preds.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284C7")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F0F9FF")]),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_preds)
    else:
        story.append(Paragraph("No prediction records found.", styles['Normal']))

    story.append(Spacer(1, 14))
    story.append(Paragraph("Physician Notes & Clinical Directives:", heading_style))
    story.append(Paragraph("This assessment is synthesized by DataVision Health machine learning algorithms across cardiometabolic and nephrological indices. Correlate with renal panel and clinical judgment before therapy initiation.", subtitle_style))
    story.append(Spacer(1, 18))
    story.append(Paragraph("Physician Signature: ___________________________    Date: ______________", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    
    filename = f"DataVision_Report_{patient.patient_code}.pdf"
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
