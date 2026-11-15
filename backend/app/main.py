import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import engine, Base
from .routers import auth, patients, records, predictions, analytics
from .ml_engine.trainer import train_and_export_models, MODELS_DIR

# Create database tables
Base.metadata.create_all(bind=engine)

# Auto-train models on initial startup if not already created
required_models = [
    "heart_disease_model.joblib",
    "diabetes_model.joblib",
    "stroke_model.joblib",
    "kidney_disease_model.joblib"
]
models_exist = all(os.path.exists(os.path.join(MODELS_DIR, m)) for m in required_models)
if not models_exist:
    print("Pre-trained models not found. Training 4 chronic disease baseline models now...")
    try:
        train_and_export_models()
    except Exception as e:
        print(f"Model training during startup deferred: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="DataVision Health: AI-Powered Healthcare Analytics & Explainable Disease Risk Prediction Platform"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(patients.router, prefix=settings.API_V1_PREFIX)
app.include_router(records.router, prefix=settings.API_V1_PREFIX)
app.include_router(predictions.router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "diseases_modeled": ["Heart Disease", "Type-2 Diabetes", "Stroke", "Chronic Kidney Disease"],
        "api_docs": "/docs"
    }

@app.get("/health")
def healthcheck():
    return {"status": "healthy"}
