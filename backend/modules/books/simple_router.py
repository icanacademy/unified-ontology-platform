from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/")
async def books_root():
    return {
        "message": "Books & Library Management Platform API",
        "version": "1.0.0",
        "description": "AI-Powered Comprehensive Library System",
        "status": "operational"
    }

@router.get("/health")
async def books_health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@router.get("/dashboard")
async def books_dashboard():
    return {
        "platform": "Books & Library Management",
        "features": [
            "Book catalog management",
            "User management and circulation", 
            "AI-powered recommendations",
            "Library analytics",
            "Advanced search capabilities"
        ],
        "stats": {
            "total_books": 0,
            "available_books": 0,
            "total_users": 0,
            "active_checkouts": 0
        }
    }