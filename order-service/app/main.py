from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as orders_router

app = FastAPI(
    title="Order Service",
    description="Smart Parking Platform - Order Management Service",
    version="1.0.0"
)

# CORS for GUI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(orders_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "order-service"}

@app.get("/")
async def root():
    return {
        "service": "order-service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "api": "/api/orders/"
        }
    }