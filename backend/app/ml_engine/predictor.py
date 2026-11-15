import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List

MODELS_DIR = os.path.dirname(os.path.abspath(__file__)) + "/models"

class HealthRiskPredictor:
    def __init__(self):
        self.models = {}
        self.metadata = None
        self._load_models()

    def _load_models(self):
        try:
            for disease in ["heart_disease", "diabetes", "stroke", "kidney_disease"]:
                path = os.path.join(MODELS_DIR, f"{disease}_model.joblib")
                if os.path.exists(path):
                    self.models[disease] = joblib.load(path)
            meta_path = os.path.join(MODELS_DIR, "models_metadata.joblib")
            if os.path.exists(meta_path):
                self.metadata = joblib.load(meta_path)
        except Exception as e:
            print(f"Warning: Models not loaded yet: {e}")

    def is_ready(self) -> bool:
        return len(self.models) >= 3

    def _format_input_dataframe(self, data: Dict[str, Any]) -> pd.DataFrame:
        gender_is_male = 1 if str(data.get("gender", "")).lower() in ["male", "m"] else 0
        smoking = 1 if data.get("smoking_status") in [True, 1, "true", "True"] else 0
        
        row = {
            "age": float(data.get("age", 45)),
            "gender_is_male": gender_is_male,
            "systolic_bp": float(data.get("systolic_bp", 120)),
            "diastolic_bp": float(data.get("diastolic_bp", 80)),
            "heart_rate": float(data.get("heart_rate", 72)),
            "fasting_glucose": float(data.get("fasting_glucose", 95)),
            "total_cholesterol": float(data.get("total_cholesterol", 190)),
            "bmi": float(data.get("bmi", 24.5)),
            "smoking": smoking,
            "physical_activity": float(data.get("physical_activity_hours", 3.0))
        }
        return pd.DataFrame([row])

    def _calculate_feature_contributions(self, model, df_row: pd.DataFrame, disease: str) -> List[Dict[str, Any]]:
        rf_classifier = model.named_steps["classifier"]
        importances = rf_classifier.feature_importances_
        feature_names = df_row.columns.tolist()

        baselines = {
            "age": 40.0,
            "gender_is_male": 0,
            "systolic_bp": 120.0,
            "diastolic_bp": 80.0,
            "heart_rate": 70.0,
            "fasting_glucose": 95.0,
            "total_cholesterol": 180.0,
            "bmi": 23.0,
            "smoking": 0,
            "physical_activity": 4.0
        }

        labels = {
            "systolic_bp": "Systolic Blood Pressure",
            "fasting_glucose": "Fasting Blood Glucose",
            "bmi": "Body Mass Index (BMI)",
            "total_cholesterol": "Total Serum Cholesterol",
            "age": "Patient Age",
            "smoking": "Tobacco Smoking",
            "physical_activity": "Weekly Physical Exercise",
            "diastolic_bp": "Diastolic Blood Pressure",
            "heart_rate": "Resting Heart Rate",
            "gender_is_male": "Biological Sex"
        }

        contributions = []
        for i, col in enumerate(feature_names):
            val = float(df_row[col].iloc[0])
            base = baselines.get(col, val)
            weight = importances[i]

            if col == "physical_activity":
                delta = base - val
            else:
                delta = val - base

            impact = delta * weight * 2.5
            impact = max(-0.4, min(0.4, impact))

            contributions.append({
                "feature": col,
                "label": labels.get(col, col),
                "patient_value": val,
                "baseline_value": base,
                "impact_score": round(float(impact), 3),
                "is_risk_driver": impact > 0.03
            })

        contributions.sort(key=lambda x: abs(x["impact_score"]), reverse=True)
        return contributions

    def _generate_recommendations(self, data: Dict[str, Any], disease: str, risk_level: str) -> List[str]:
        recs = []
        sbp = float(data.get("systolic_bp", 120))
        glucose = float(data.get("fasting_glucose", 95))
        bmi = float(data.get("bmi", 24))
        chol = float(data.get("total_cholesterol", 190))
        smoking = data.get("smoking_status") in [True, 1, "true", "True"]
        activity = float(data.get("physical_activity_hours", 3.0))

        if disease == "kidney_disease":
            if sbp >= 130:
                recs.append("Strict BP management (< 125/80 mmHg) recommended to mitigate renal hyperfiltration injury.")
            if glucose >= 110:
                recs.append("Rigorous glycemic control required to prevent progressive diabetic microvascular nephropathy.")
            recs.append("Screen annually for microalbuminuria and serum creatinine / eGFR decline.")
            if bmi >= 28:
                recs.append("Adopt a kidney-friendly low-sodium Mediterranean nutritional regimen.")

        if smoking:
            recs.append("Enroll in tobacco cessation program to cut cardiovascular, renal & stroke hazards by up to 50%.")
        if sbp >= 135 and disease != "kidney_disease":
            recs.append(f"Systolic BP is elevated ({sbp} mmHg). Adopt a low-sodium DASH diet and track daily BP.")
        if glucose >= 115 and disease != "kidney_disease":
            recs.append(f"Fasting glucose is high ({glucose} mg/dL). Restrict refined carbohydrates and request HbA1c test.")
        if bmi >= 27 and disease != "kidney_disease":
            recs.append(f"BMI indicates overweight status ({bmi:.1f} kg/m²). Target a progressive 5-7% weight reduction.")
        if activity < 2.5:
            recs.append("Increase aerobic physical exercise to at least 150 minutes per week.")

        if not recs:
            recs.append("Vitals are well-controlled within normal clinical bounds. Maintain healthy lifestyle routine.")

        return recs[:4]

    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_ready():
            self._load_models()

        df_row = self._format_input_dataframe(data)
        results = {}
        total_risk = 0.0

        for disease, model in self.models.items():
            prob = float(model.predict_proba(df_row)[0, 1])
            percentage = round(prob * 100, 1)

            if prob < 0.25:
                level = "LOW"
                color = "#10B981"
            elif prob < 0.55:
                level = "MODERATE"
                color = "#F59E0B"
            elif prob < 0.75:
                level = "HIGH"
                color = "#F97316"
            else:
                level = "CRITICAL"
                color = "#EF4444"

            contributions = self._calculate_feature_contributions(model, df_row, disease)
            recs = self._generate_recommendations(data, disease, level)

            name_map = {
                "heart_disease": "Heart Disease",
                "diabetes": "Type-2 Diabetes",
                "stroke": "Stroke Probability",
                "kidney_disease": "Kidney Disease (CKD)"
            }

            results[disease] = {
                "disease_type": name_map.get(disease, disease.replace("_", " ").title()),
                "risk_score": round(prob, 4),
                "risk_percentage": percentage,
                "risk_level": level,
                "color": color,
                "feature_contributions": contributions[:5],
                "clinical_recommendations": recs
            }
            total_risk += prob

        avg_risk = total_risk / max(len(self.models), 1)
        overall_health_score = max(0, min(100, round((1.0 - avg_risk) * 100, 1)))

        return {
            "overall_health_score": overall_health_score,
            "risks": results
        }

    def simulate_what_if(self, baseline_data: Dict[str, Any], modified_params: Dict[str, Any]) -> Dict[str, Any]:
        simulated_data = baseline_data.copy()
        simulated_data.update(modified_params)

        baseline_res = self.predict(baseline_data)
        simulated_res = self.predict(simulated_data)

        deltas = {}
        for disease in self.models.keys():
            base_pct = baseline_res["risks"].get(disease, {}).get("risk_percentage", 0)
            sim_pct = simulated_res["risks"].get(disease, {}).get("risk_percentage", 0)
            deltas[disease] = round(sim_pct - base_pct, 1)

        return {
            "baseline_risks": baseline_res["risks"],
            "simulated_risks": simulated_res["risks"],
            "risk_delta": deltas,
            "baseline_health_score": baseline_res["overall_health_score"],
            "simulated_health_score": simulated_res["overall_health_score"]
        }

predictor = HealthRiskPredictor()
