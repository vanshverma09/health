import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "DataVision Health"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "datavision-health-super-secret-jwt-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    
    # Database (Default to local SQLite for seamless zero-config setup)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./datavision.db")
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]

settings = Settings()

