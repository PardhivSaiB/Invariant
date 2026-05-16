from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI DSA Mentor"
    API_V1_STR: str = "/api"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Google Gemini Configuration
    GEMINI_API_KEY: str = ""
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost/dsamentor"
    
    ENV: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()
