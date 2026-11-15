# DataVision Health
### *AI-Powered Healthcare Analytics & Explainable Disease Risk Prediction Platform*

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19.0-61DAFB.svg)](https://react.dev)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v4.0-38B2AC.svg)](https://tailwindcss.com)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E.svg)](https://scikit-learn.org)

**DataVision Health** is an end-to-end clinical intelligence platform combining **longitudinal physiological biomarker telemetry** with **multi-disease machine learning (Heart Disease, Diabetes, Stroke)** and **Explainable AI (XAI)**.

---

## 🌟 Key Features

1. **Longitudinal Biomarker "Data Vision":** Interactive multi-series clinical charts (Recharts) mapping patient vitals (Blood Pressure, Glucose, BMI, Cholesterol) over time with color-coded safety thresholds.
2. **Multi-Disease Risk AI:** Concurrent probability risk scoring across three major chronic non-communicable conditions (Heart Disease, Type-2 Diabetes, Stroke).
3. **Explainable AI (XAI) Attribution:** Custom SHAP-grounded diverging bar charts that decompose the black-box risk score into exact positive and negative biomarker contributors.
4. **Interactive "What-If" Counterfactual Prognosis Lab:** Real-time sliders allowing clinicians to simulate targeted therapeutic interventions (e.g., reducing systolic BP, 5% weight loss, smoking cessation) and observe quantified risk deltas ($\Delta \text{Risk}$).
5. **Population Health Observatory:** Epidemiological cohort charts showing demographic age distributions and chronic disease prevalence percentages.
6. **Automated PDF Clinical Reports:** One-click generation of professional medical summaries via ReportLab, ready for patient discharge and physician sign-off.
7. **Stateless JWT Security & RBAC:** Role-based access control protecting clinical routes with BCrypt encrypted credentials.

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (DATA VISION UI)                      │
│       React 19 + Vite + Tailwind CSS v4 + Recharts + Lucide Icons      │
│   • Clinical Overview  • Patient Directory  • XAI Diagnostics Suite   │
│   • What-If Lifestyle Lab  • Hospital Population Observatory          │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │ RESTful API (JSON / Bearer JWT)
┌────────────────────────────────────▼───────────────────────────────────┐
│                     BACKEND (API & BUSINESS LOGIC)                     │
│                            Python 3.12 FastAPI                         │
│   • JWT Auth & Security                 • Patient & Vitals CRUD       │
│   • Pydantic Input Validation           • ReportLab PDF Generator     │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │                                 │
┌──────────────────▼───────────────┐ ┌───────────────▼───────────────────┐
│          DATABASE TIER           │ │          ML & XAI ENGINE          │
│       SQLAlchemy (SQLite)        │ │      Scikit-learn + SHAP XAI      │
│  • Users & Profiles              │ │  • Random Forest Ensembles        │
│  • Longitudinal Health Records   │ │  • Calibrated Probabilities       │
│  • Historical Prediction Logs    │ │  • Biomarker Attribution Vectors  │
└──────────────────────────────────┘ └───────────────────────────────────┘
```

---

## ⚡ Quick Start Guide

### Prerequisites
* **Python 3.10+** (Python 3.12 recommended)
* **Node.js v18+** and **npm**

---

### Step 1: Backend Setup & Launch

```powershell
# 1. Navigate to backend directory
cd backend

# 2. Activate virtual environment (Windows)
.\.venv\Scripts\Activate.ps1
# (On macOS/Linux: source .venv/bin/activate)

# 3. Seed demo patients & train models (One-time setup)
python -m app.seed_data

# 4. Start the FastAPI development server
python -m uvicorn app.main:app --reload --port 8000
```
> **Backend API Docs:** Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser for the interactive Swagger UI.

---

### Step 2: Frontend Setup & Launch

Open a second terminal window:

```powershell
# 1. Navigate to frontend directory
cd frontend

# 2. Start the Vite development server
npm run dev
```
> **Web Application:** Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🔑 Demo Login Credentials

The database comes pre-seeded with 8 diverse clinical profiles and an attending physician account:

* **Clinician Email:** `doctor@datavision.com`
* **Password:** `password123`
*(A convenient one-click "Pre-fill" button is also provided directly on the login screen).*

---

## 📂 Project Organization

```
DATA VISION/
├── backend/
│   ├── app/
│   │   ├── ml_engine/
│   │   │   ├── trainer.py           # ML training pipeline for 3 diseases
│   │   │   ├── predictor.py         # Inference & SHAP attribution service
│   │   │   └── models/              # Serialized .joblib model artifacts
│   │   ├── routers/
│   │   │   ├── auth.py              # Login & registration routes
│   │   │   ├── patients.py          # Patient directory & profile routes
│   │   │   ├── records.py           # Vitals ingestion & timeline routes
│   │   │   ├── predictions.py       # Disease risk AI & What-If endpoints
│   │   │   └── analytics.py         # Cohort analytics & PDF export
│   │   ├── auth.py                  # JWT creation & verification
│   │   ├── config.py                # Environment configurations
│   │   ├── database.py              # SQLAlchemy engine & session
│   │   ├── models.py                # Database ORM models
│   │   ├── schemas.py               # Pydantic validation schemas
│   │   ├── seed_data.py             # 8 pre-configured patients & history
│   │   └── main.py                  # FastAPI application entrypoint
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx          # Modern clinical navigation
│   │   │   ├── RiskGauge.jsx        # Semicircular animated SVG gauge
│   │   │   ├── ShapExplainer.jsx    # Diverging XAI attribution bars
│   │   │   ├── VitalsTimeline.jsx   # Multi-series Recharts trajectory
│   │   │   ├── WhatIfSimulator.jsx  # Interactive counterfactual lab
│   │   │   ├── NewPatientModal.jsx  # Patient registration modal
│   │   │   └── NewRecordModal.jsx   # Checkup vitals entry modal
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx        # Clinical command center
│   │   │   ├── Patients.jsx         # Searchable patient directory
│   │   │   ├── PredictiveDiagnostics.jsx # AI risk & XAI suite
│   │   │   ├── PopulationAnalytics.jsx   # Epidemiological observatory
│   │   │   └── Login.jsx            # Secure authentication page
│   │   ├── services/
│   │   │   └── api.js               # Centralized REST client
│   │   ├── App.jsx                  # Main view router
│   │   └── main.jsx
│   └── package.json
└── docs/
    ├── COLLEGE_REPORT.md            # Complete 7-chapter academic report
    └── VIVA_QUESTIONS.md            # 25 Viva defense questions & answers
```

---

## 🎓 Academic Deliverables
* **Comprehensive Project Report:** Detailed university submission document in [docs/COLLEGE_REPORT.md](docs/COLLEGE_REPORT.md).
* **Viva Voce Defense Guide:** Examiner Q&A guide covering ML mechanics, XAI mathematical formulas, and system design in [docs/VIVA_QUESTIONS.md](docs/VIVA_QUESTIONS.md).

