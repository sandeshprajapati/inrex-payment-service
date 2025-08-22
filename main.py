from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api import wallet
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI app
app = FastAPI(
    title="Payment Wallet Service",
    description="A REST API service for managing user wallets and transactions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include wallet routes
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet Operations"])

@app.get("/", tags=["Health"])
def root():
    """Health check endpoint"""
    return {
        "message": "Payment Wallet Service is running",
        "status": "healthy",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health check"""
    return {
        "service": "Payment Wallet Service",
        "status": "healthy",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
