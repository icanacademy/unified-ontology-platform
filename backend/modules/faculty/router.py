from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from . import crud, models, schemas
from .database import SessionLocal, engine
from .ai_service import faculty_ai_service
from .data_import import faculty_import_service
from pydantic import BaseModel
from .profile_models import FacultyProfile, FacultyEvaluation, PerformanceMetric, FacultyGoal, ProfessionalDevelopment
import profile_schemas

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def faculty_root():
    return {"message": "Faculty Performance & Research Analytics Platform API"}

@router.get("/health")
async def faculty_health_check():
    return {"status": "healthy"}

# Faculty Management Endpoints
@router.post("/faculty/", response_model=schemas.Faculty)
def create_faculty(faculty: schemas.FacultyCreate, db: Session = Depends(get_db)):
    db_faculty = crud.get_faculty_by_faculty_id(db, faculty_id=faculty.faculty_id)
    if db_faculty:
        raise HTTPException(status_code=400, detail="Faculty ID already registered")
    return crud.create_faculty(db=db, faculty=faculty)

@router.get("/faculty/", response_model=List[schemas.Faculty])
def read_faculty(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    faculty = crud.get_faculty_list(db, skip=skip, limit=limit)
    return faculty

@router.get("/faculty/{faculty_id}", response_model=schemas.Faculty)
def read_faculty_member(faculty_id: int, db: Session = Depends(get_db)):
    db_faculty = crud.get_faculty(db, faculty_id=faculty_id)
    if db_faculty is None:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    return db_faculty

@router.get("/faculty/{faculty_id}/analytics", response_model=schemas.FacultyPerformanceAnalytics)
def get_faculty_analytics(faculty_id: int, db: Session = Depends(get_db)):
    faculty = crud.get_faculty(db, faculty_id=faculty_id)
    if faculty is None:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    
    # Get comprehensive analytics
    research_metrics = crud.get_faculty_research_metrics(db, faculty_id)
    teaching_metrics = crud.get_faculty_teaching_metrics(db, faculty_id)
    service_metrics = crud.get_faculty_service_metrics(db, faculty_id)
    overall_scores = crud.get_faculty_overall_scores(db, faculty_id)
    recent_achievements = crud.get_faculty_recent_achievements(db, faculty_id)
    
    # Get AI-generated insights
    improvement_areas = crud.get_faculty_insights(db, faculty_id, "weakness")
    recommendations = crud.get_faculty_insights(db, faculty_id, "recommendation")
    
    return schemas.FacultyPerformanceAnalytics(
        faculty=faculty,
        research_metrics=research_metrics,
        teaching_metrics=teaching_metrics,
        service_metrics=service_metrics,
        overall_scores=overall_scores,
        recent_achievements=recent_achievements,
        improvement_areas=improvement_areas,
        recommendations=recommendations
    )

# Research Management Endpoints
@router.post("/research/", response_model=schemas.Research)
def create_research(research: schemas.ResearchCreate, db: Session = Depends(get_db)):
    return crud.create_research(db=db, research=research)

@router.get("/research/faculty/{faculty_id}", response_model=List[schemas.Research])
def read_faculty_research(faculty_id: int, db: Session = Depends(get_db)):
    research = crud.get_faculty_research(db, faculty_id=faculty_id)
    return research

# Teaching Management Endpoints  
@router.post("/teaching/", response_model=schemas.Teaching)
def create_teaching(teaching: schemas.TeachingCreate, db: Session = Depends(get_db)):
    return crud.create_teaching(db=db, teaching=teaching)

@router.get("/teaching/faculty/{faculty_id}", response_model=List[schemas.Teaching])
def read_faculty_teaching(faculty_id: int, db: Session = Depends(get_db)):
    teaching = crud.get_faculty_teaching(db, faculty_id=faculty_id)
    return teaching

# AI Analysis Endpoints
@router.post("/faculty/{faculty_id}/analyze")
def analyze_faculty_performance(faculty_id: int, db: Session = Depends(get_db)):
    faculty = crud.get_faculty(db, faculty_id=faculty_id)
    if faculty is None:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    
    insights = faculty_ai_service.analyze_faculty_performance(db, faculty_id)
    
    # Save insights to database
    saved_insights = []
    for insight in insights:
        saved_insight = crud.create_faculty_insight(db, insight)
        saved_insights.append(saved_insight)
    
    return {"message": f"Generated {len(saved_insights)} insights for faculty member", "insights": saved_insights}

# Department Analytics Endpoints
@router.get("/analytics/department/{department}")
def get_department_analytics(department: str, db: Session = Depends(get_db)):
    analytics = crud.get_department_analytics(db, department)
    return analytics

@router.get("/analytics/dashboard")
def get_faculty_dashboard_analytics(db: Session = Depends(get_db)):
    stats = crud.get_dashboard_stats(db)
    research_overview = crud.get_research_overview(db)
    teaching_overview = crud.get_teaching_overview(db)
    collaboration_network = crud.get_collaboration_network_stats(db)
    top_performers = crud.get_top_performers(db)
    
    return {
        "overview": stats,
        "research_overview": research_overview,
        "teaching_overview": teaching_overview,
        "collaboration_network": collaboration_network,
        "top_performers": top_performers
    }

# Data Import Endpoints
class ImportData(BaseModel):
    data: str

@router.post("/import/faculty")
def import_faculty_data(import_data: ImportData, db: Session = Depends(get_db)):
    result = faculty_import_service.import_faculty(db, import_data.data)
    return result

@router.post("/import/research")
def import_research_data(import_data: ImportData, db: Session = Depends(get_db)):
    result = faculty_import_service.import_research(db, import_data.data)
    return result