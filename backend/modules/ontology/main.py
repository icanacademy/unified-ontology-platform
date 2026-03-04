from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Dict, Any
import os
import subprocess
import json
from pathlib import Path
from pydantic import BaseModel
import asyncio

app = FastAPI(
    title="Dr. ICAN Ontology Platform",
    description="Central launcher for ontology-based applications",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3002", "http://localhost:3001", "http://localhost:3000", "http://localhost:3003", "http://localhost:3004", "http://localhost:3005"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Application registry
APPLICATIONS = [
    {
        "id": "student-analytics",
        "name": "Student Analytics Platform", 
        "description": "Comprehensive educational analytics with AI-powered insights",
        "version": "1.0.0",
        "status": "available",
        "domain": "Education",
        "entities": ["Students", "Teachers", "Courses", "Assessments"],
        "ai_features": ["Performance Analysis", "Teaching Recommendations", "Risk Detection"],
        "icon": "🎓",
        "color": "#1976d2",
        "path": "../student-analytics-platform",
        "frontend_port": 3001,
        "backend_port": 8001,
        "launch_command": "python one-click-setup.py"
    },
    {
        "id": "faculty-analytics",
        "name": "ESL Teacher Performance & Development Analytics",
        "description": "Comprehensive ESL teacher evaluation with AI-powered teaching insights and professional development tracking",
        "version": "1.0.0", 
        "status": "available",
        "domain": "ESL Teaching Excellence",
        "entities": ["ESL Teachers", "Students", "Evaluations", "Professional Development", "Goals"],
        "ai_features": ["Teaching Performance Analysis", "Student Progress Tracking", "Professional Development Recommendations", "Cultural Competency Assessment"],
        "icon": "🎯",
        "color": "#4527a0",
        "path": "../faculty-analytics-platform",
        "frontend_port": 3003,
        "backend_port": 8003,
        "launch_command": "python simple-start.py"
    },
    {
        "id": "books-library",
        "name": "Books & Library Management Platform",
        "description": "Comprehensive library management system with AI-powered book recommendations, circulation tracking, and advanced analytics",
        "version": "1.0.0",
        "status": "available", 
        "domain": "Library & Information Science",
        "entities": ["Books", "Authors", "Users", "Checkouts", "Reservations", "Reviews", "Collections", "Events"],
        "ai_features": ["Smart Book Recommendations", "Reading Analytics", "Content Analysis", "User Behavior Insights", "Inventory Optimization"],
        "icon": "📚",
        "color": "#2e7d32",
        "path": "../books-library-platform",
        "frontend_port": 3004,
        "backend_port": 8004,
        "launch_command": "python simple-start.py"
    },
    {
        "id": "ican-class-management",
        "name": "ICAN Class Management & Curriculum Analytics",
        "description": "Comprehensive ESL curriculum management with AI-powered class recommendations, progress tracking, and learning pathway optimization for all 19 ICAN classes",
        "version": "1.0.0",
        "status": "available",
        "domain": "ESL Curriculum & Class Management",
        "entities": ["Classes", "Curricula", "Learning Levels", "Class Schedules", "Student Enrollments", "Learning Objectives", "Course Materials", "Assessments", "Learning Paths"],
        "ai_features": ["Class Level Recommendations", "Learning Path Optimization", "Progress Prediction", "Curriculum Gap Analysis", "Student-Class Matching"],
        "icon": "🎓",
        "color": "#9c27b0",
        "path": "../ican-class-management-platform",
        "frontend_port": 3005,
        "backend_port": 8005,
        "launch_command": "python one-click-setup.py"
    }
]

class ApplicationStatus(BaseModel):
    id: str
    status: str  # available, running, stopped, error
    frontend_url: str = None
    backend_url: str = None

# Store running application processes
running_processes = {}

@app.get("/")
async def root():
    return {
        "message": "Dr. ICAN Ontology Platform - Central Command",
        "version": "1.0.0",
        "applications_count": len(APPLICATIONS)
    }

@app.get("/applications", response_model=List[Dict[str, Any]])
async def get_applications():
    """Get list of all available ontology applications"""
    return APPLICATIONS

@app.get("/applications/{app_id}")
async def get_application(app_id: str):
    """Get details of a specific application"""
    app = next((a for a in APPLICATIONS if a["id"] == app_id), None)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@app.post("/applications/{app_id}/launch")
async def launch_application(app_id: str):
    """Launch a specific ontology application"""
    app = next((a for a in APPLICATIONS if a["id"] == app_id), None)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check if app is already running
    if app_id in running_processes:
        return {
            "message": f"{app['name']} is already running",
            "status": "running",
            "frontend_url": f"http://localhost:{app['frontend_port']}",
            "backend_url": f"http://localhost:{app['backend_port']}"
        }
    
    try:
        # Launch the application
        app_path = Path(__file__).parent.parent / app["path"]
        if not app_path.exists():
            raise HTTPException(status_code=404, detail="Application path not found")
        
        # Start the application process
        process = subprocess.Popen(
            app["launch_command"],
            shell=True,
            cwd=app_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        running_processes[app_id] = {
            "process": process,
            "app": app
        }
        
        return {
            "message": f"Launching {app['name']}...",
            "status": "starting",
            "frontend_url": f"http://localhost:{app['frontend_port']}",
            "backend_url": f"http://localhost:{app['backend_port']}",
            "estimated_startup_time": "30-60 seconds"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to launch application: {str(e)}")

@app.post("/applications/{app_id}/stop")
async def stop_application(app_id: str):
    """Stop a running application"""
    if app_id not in running_processes:
        raise HTTPException(status_code=404, detail="Application is not running")
    
    try:
        process_info = running_processes[app_id]
        process = process_info["process"]
        app = process_info["app"]
        
        # Terminate the process
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
        
        del running_processes[app_id]
        
        return {
            "message": f"{app['name']} stopped successfully",
            "status": "stopped"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop application: {str(e)}")

@app.get("/applications/{app_id}/status")
async def get_application_status(app_id: str):
    """Get the current status of an application"""
    app = next((a for a in APPLICATIONS if a["id"] == app_id), None)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if app_id in running_processes:
        process_info = running_processes[app_id]
        process = process_info["process"]
        
        # Check if process is still running
        if process.poll() is None:
            return ApplicationStatus(
                id=app_id,
                status="running",
                frontend_url=f"http://localhost:{app['frontend_port']}",
                backend_url=f"http://localhost:{app['backend_port']}"
            )
        else:
            # Process died, clean up
            del running_processes[app_id]
            return ApplicationStatus(id=app_id, status="stopped")
    
    return ApplicationStatus(id=app_id, status="available")

@app.get("/analytics/overview")
async def get_platform_analytics():
    """Get overview analytics across all ontology applications"""
    total_apps = len(APPLICATIONS)
    running_apps = len(running_processes)
    available_apps = total_apps - running_apps
    
    # Count entities across all applications
    all_entities = set()
    for app in APPLICATIONS:
        all_entities.update(app.get("entities", []))
    
    # Count AI features
    all_ai_features = set()
    for app in APPLICATIONS:
        all_ai_features.update(app.get("ai_features", []))
    
    return {
        "platform": {
            "name": "Dr. ICAN Ontology Platform",
            "version": "1.0.0",
            "applications": {
                "total": total_apps,
                "running": running_apps,
                "available": available_apps
            }
        },
        "ontology": {
            "total_entity_types": len(all_entities),
            "entity_types": list(all_entities),
            "ai_features": list(all_ai_features)
        },
        "domains": list(set(app.get("domain", "General") for app in APPLICATIONS))
    }

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up running processes on shutdown"""
    for app_id, process_info in running_processes.items():
        process = process_info["process"]
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

# Serve the frontend
if os.path.exists("../frontend/build"):
    app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404)
        return FileResponse("../frontend/build/index.html")