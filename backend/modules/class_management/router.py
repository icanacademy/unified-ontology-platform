from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud
from . import models
from . import schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def classes_root():
    return {
        "message": "ICAN Class Management Platform API",
        "version": "1.0.0",
        "features": ["Class Management", "Student Tracking", "AI Recommendations", "Learning Paths"]
    }

# Class Categories
@router.get("/categories", response_model=List[schemas.ClassCategory])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_class_categories(db, skip=skip, limit=limit)

@router.post("/categories", response_model=schemas.ClassCategory)
def create_category(category: schemas.ClassCategoryCreate, db: Session = Depends(get_db)):
    return crud.create_class_category(db, category)

# Classes
@router.get("/classes", response_model=List[schemas.Class])
def read_classes(skip: int = 0, limit: int = 100, category_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_classes(db, skip=skip, limit=limit, category_id=category_id)

@router.get("/classes/{class_id}", response_model=schemas.Class)
def read_class(class_id: int, db: Session = Depends(get_db)):
    db_class = crud.get_class(db, class_id=class_id)
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class

@router.post("/classes", response_model=schemas.Class)
def create_class(class_data: schemas.ClassCreate, db: Session = Depends(get_db)):
    return crud.create_class(db, class_data)

@router.put("/classes/{class_id}", response_model=schemas.Class)
def update_class(class_id: int, class_data: schemas.ClassCreate, db: Session = Depends(get_db)):
    db_class = crud.get_class(db, class_id=class_id)
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return crud.update_class(db, class_id, class_data)

# Students
@router.get("/students", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_students(db, skip=skip, limit=limit)

@router.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.post("/students", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_email(db, email=student.email)
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db, student)

# Student Progress
@router.get("/students/{student_id}/progress", response_model=List[schemas.StudentProgress])
def read_student_progress(student_id: int, db: Session = Depends(get_db)):
    return crud.get_student_progress(db, student_id)

@router.post("/progress", response_model=schemas.StudentProgress)
def create_progress(progress: schemas.StudentProgressCreate, db: Session = Depends(get_db)):
    return crud.create_student_progress(db, progress)

# Learning Paths
@router.get("/learning-paths", response_model=List[schemas.LearningPath])
def read_learning_paths(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_learning_paths(db, skip=skip, limit=limit)

@router.post("/learning-paths", response_model=schemas.LearningPath)
def create_learning_path(path: schemas.LearningPathCreate, db: Session = Depends(get_db)):
    return crud.create_learning_path(db, path)

# AI Recommendations
@router.get("/students/{student_id}/recommendations", response_model=List[schemas.ClassRecommendation])
def get_recommendations(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return crud.get_class_recommendations(db, student_id)

# Dashboard
@router.get("/dashboard/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)

@router.get("/analytics/overview")
def get_analytics_overview(db: Session = Depends(get_db)):
    stats = crud.get_dashboard_stats(db)
    return {
        "platform": {
            "name": "ICAN Class Management",
            "version": "1.0.0",
            "total_classes": stats.total_classes,
            "total_students": stats.total_students,
            "completion_rate": stats.completion_rate
        },
        "class_categories": [
            "Reading Track", "Writing Track", "Speaking Track", 
            "Test Preparation", "Advanced Courses", "STEM"
        ],
        "popular_classes": stats.popular_classes
    }