from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Payment Wallet Service"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/payment"
    
    class Config:
        case_sensitive = True

settings = Settings()
