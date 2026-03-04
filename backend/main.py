from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import platform routers with error handling
routers = {}

# Try to load full routers first, fallback to simple versions
try:
    from modules.books.router import router as books_router
    routers['books'] = books_router
    logger.info("✅ Books platform (full) loaded")
except Exception as e:
    try:
        from modules.books.simple_router import router as books_router
        routers['books'] = books_router
        logger.info("✅ Books platform (simple) loaded")
    except Exception as e2:
        logger.warning(f"⚠️ Books platform not available: {e2}")

try:
    from modules.faculty.router import router as faculty_router
    routers['faculty'] = faculty_router
    logger.info("✅ Faculty platform (full) loaded")
except Exception as e:
    try:
        from modules.faculty.simple_router import router as faculty_router
        routers['faculty'] = faculty_router
        logger.info("✅ Faculty platform (simple) loaded")
    except Exception as e2:
        logger.warning(f"⚠️ Faculty platform not available: {e2}")

try:
    from modules.student.router import router as student_router
    routers['students'] = student_router
    logger.info("✅ Student platform (full) loaded")
except Exception as e:
    try:
        from modules.student.simple_router import router as student_router
        routers['students'] = student_router
        logger.info("✅ Student platform (simple) loaded")
    except Exception as e2:
        logger.warning(f"⚠️ Student platform not available: {e2}")

try:
    from modules.class_management.router import router as classes_router
    routers['classes'] = classes_router
    logger.info("✅ Classes platform (full) loaded")
except Exception as e:
    try:
        from modules.class_management.simple_router import router as classes_router
        routers['classes'] = classes_router
        logger.info("✅ Classes platform (simple) loaded")
    except Exception as e2:
        logger.warning(f"⚠️ Classes platform not available: {e2}")

try:
    from modules.ontology.router import router as ontology_router
    routers['ontology'] = ontology_router
    logger.info("✅ Ontology platform loaded")
except Exception as e:
    logger.warning(f"⚠️ Ontology platform not available: {e}")

app = FastAPI(
    title="Unified Ontology Platform",
    description="Integrated Educational Analytics Platform - Books, Faculty, Students, Classes & Ontology",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for all platforms
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", "http://localhost:3001", "http://localhost:3002", 
        "http://localhost:3003", "http://localhost:3004", "http://localhost:3005",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount platform routers with prefixes - only if they loaded successfully
if 'books' in routers:
    app.include_router(routers['books'], prefix="/api/books", tags=["Books Library Platform"])
if 'faculty' in routers:
    app.include_router(routers['faculty'], prefix="/api/faculty", tags=["Faculty Analytics Platform"])
if 'students' in routers:
    app.include_router(routers['students'], prefix="/api/students", tags=["Student Analytics Platform"])
if 'classes' in routers:
    app.include_router(routers['classes'], prefix="/api/classes", tags=["Class Management Platform"])
if 'ontology' in routers:
    app.include_router(routers['ontology'], prefix="/api/ontology", tags=["Ontology Platform"])

@app.get("/")
async def root():
    available_platforms = {}
    for platform, path in [
        ("books", "/api/books"),
        ("faculty", "/api/faculty"), 
        ("students", "/api/students"),
        ("classes", "/api/classes"),
        ("ontology", "/api/ontology")
    ]:
        if platform in routers:
            available_platforms[platform] = path
    
    return {
        "message": "Unified Ontology Platform",
        "version": "1.0.0",
        "platforms": available_platforms,
        "docs": "/api/docs",
        "status": "operational",
        "loaded_modules": len(routers)
    }

@app.get("/health")
async def health_check():
    platform_status = {}
    for platform in ["books", "faculty", "students", "classes", "ontology"]:
        platform_status[platform] = "operational" if platform in routers else "not_loaded"
    
    return {
        "status": "healthy",
        "platforms": platform_status,
        "loaded_modules": len(routers)
    }

@app.get("/api/dashboard")
async def unified_dashboard():
    """Unified dashboard with links to all platforms"""
    return {
        "title": "Unified Educational Analytics Dashboard",
        "platforms": [
            {
                "name": "Books & Library",
                "description": "Comprehensive library management with AI-powered features",
                "url": "/api/books",
                "icon": "📚",
                "status": "active"
            },
            {
                "name": "Faculty Analytics", 
                "description": "Faculty performance and research analytics platform",
                "url": "/api/faculty",
                "icon": "👨‍🏫",
                "status": "active"
            },
            {
                "name": "Student Analytics",
                "description": "Student performance tracking and analytics",
                "url": "/api/students", 
                "icon": "🎓",
                "status": "active"
            },
            {
                "name": "Class Management",
                "description": "ESL curriculum and class management system",
                "url": "/api/classes",
                "icon": "📋",
                "status": "active"
            },
            {
                "name": "Ontology Platform",
                "description": "Advanced ontology management and analysis",
                "url": "/api/ontology",
                "icon": "🧠",
                "status": "active"
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)