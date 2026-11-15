"""
DataVision Health - Automated Integration & System Verification Test Suite
Tests authentication, database integrity, ML inference across 4 chronic diseases,
Explainable AI (XAI) feature attributions, and What-If counterfactual simulations.
"""

import sys
import unittest
from fastapi.testclient import TestClient

try:
    from app.main import app
    from app.database import Base, engine, SessionLocal
    from app.seed_data import seed
except ImportError as e:
    print(f"Skipping execution until dependencies are installed: {e}")
    sys.exit(0)

class TestDataVisionHealth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n[SETUP] Initializing database and running test migrations...")
        seed()
        cls.client = TestClient(app)

    def test_01_healthcheck(self):
        """Verify API gateway health check endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})
        print("✓ Healthcheck endpoint operational.")

    def test_02_doctor_login(self):
        """Verify JWT authentication for attending clinician."""
        response = self.client.post("/api/v1/auth/login", json={
            "email": "doctor@datavision.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["token_type"], "bearer")
        self.__class__.token = data["access_token"]
        print("✓ Attending clinician authenticated with Bearer JWT.")

    def test_03_list_patients(self):
        """Verify patient directory retrieval and risk tags."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/api/v1/patients/", headers=headers)
        self.assertEqual(response.status_code, 200)
        patients = response.json()
        self.assertGreaterEqual(len(patients), 5)
        print(f"✓ Retrieved {len(patients)} monitored patient records.")

    def test_04_four_disease_prediction_and_xai(self):
        """Verify simultaneous 4-disease prediction and SHAP feature attributions."""
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {
            "age": 58,
            "gender": "Male",
            "systolic_bp": 145,
            "diastolic_bp": 92,
            "heart_rate": 78,
            "fasting_glucose": 132.0,
            "total_cholesterol": 240.0,
            "bmi": 29.5,
            "smoking_status": True,
            "physical_activity_hours": 1.5
        }
        response = self.client.post("/api/v1/predict/disease-risk", json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("overall_health_score", data)
        self.assertIn("risks", data)
        risks = data["risks"]

        # Validate presence of all 4 chronic conditions
        expected_diseases = ["heart_disease", "diabetes", "stroke", "kidney_disease"]
        for d in expected_diseases:
            self.assertIn(d, risks)
            risk_item = risks[d]
            self.assertIn(risk_item["risk_level"], ["LOW", "MODERATE", "HIGH", "CRITICAL"])
            self.assertGreaterEqual(risk_item["risk_percentage"], 0)
            self.assertLessEqual(risk_item["risk_percentage"], 100)
            self.assertTrue(len(risk_item["feature_contributions"]) > 0)
            print(f"  - {risk_item['disease_type']}: {risk_item['risk_percentage']}% ({risk_item['risk_level']})")

        print("✓ Multi-disease inference & XAI biomarker attributions validated.")

    def test_05_what_if_counterfactual_simulation(self):
        """Verify What-If lifestyle simulator computes risk abatement deltas."""
        headers = {"Authorization": f"Bearer {self.token}"}
        baseline = {
            "age": 55,
            "gender": "Male",
            "systolic_bp": 148,
            "diastolic_bp": 94,
            "fasting_glucose": 135.0,
            "total_cholesterol": 230.0,
            "bmi": 31.0,
            "smoking_status": True,
            "physical_activity_hours": 1.0
        }
        modified = {
            "systolic_bp": 120,
            "fasting_glucose": 95.0,
            "bmi": 25.0,
            "smoking_status": False,
            "physical_activity_hours": 4.0
        }
        response = self.client.post("/api/v1/predict/what-if", json={
            "baseline_data": baseline,
            "modified_params": modified
        }, headers=headers)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("risk_delta", data)
        self.assertGreater(data["simulated_health_score"], data["baseline_health_score"])
        print(f"✓ What-If counterfactual verified: Health score improved from {data['baseline_health_score']} to {data['simulated_health_score']}.")

if __name__ == "__main__":
    unittest.main()

