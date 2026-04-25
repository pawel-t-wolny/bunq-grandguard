from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import scam_detection, webhooks
import logging

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = FastAPI(
    title="bunq Hackathon API",
    description="FastAPI backend integrating with bunq_client.py",
    version="1.0.0"
)

# CORS middleware for a frontend (allow everything for Hackathon speed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include webhook router
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
app.include_router(scam_detection.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the bunq Hackathon API! Backend is running.",
        "docs": "/docs",
        "scam_check_endpoint": "/api/v1/scam/check",
    }
