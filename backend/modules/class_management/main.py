from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ICAN Class Management Platform",
    description="Comprehensive ESL curriculum management with AI-powered recommendations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3005", "http://localhost:3000", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {
        "message": "ICAN Class Management Platform API",
        "version": "1.0.0",
        "features": ["Class Management", "Student Tracking", "AI Recommendations", "Learning Paths"]
    }

# Class Categories
@app.get("/categories", response_model=List[schemas.ClassCategory])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_class_categories(db, skip=skip, limit=limit)

@app.post("/categories", response_model=schemas.ClassCategory)
def create_category(category: schemas.ClassCategoryCreate, db: Session = Depends(get_db)):
    return crud.create_class_category(db, category)

# Classes
@app.get("/classes", response_model=List[schemas.Class])
def read_classes(skip: int = 0, limit: int = 100, category_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_classes(db, skip=skip, limit=limit, category_id=category_id)

@app.get("/classes/{class_id}", response_model=schemas.Class)
def read_class(class_id: int, db: Session = Depends(get_db)):
    db_class = crud.get_class(db, class_id=class_id)
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_class

@app.post("/classes", response_model=schemas.Class)
def create_class(class_data: schemas.ClassCreate, db: Session = Depends(get_db)):
    return crud.create_class(db, class_data)

@app.put("/classes/{class_id}", response_model=schemas.Class)
def update_class(class_id: int, class_data: schemas.ClassCreate, db: Session = Depends(get_db)):
    db_class = crud.get_class(db, class_id=class_id)
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return crud.update_class(db, class_id, class_data)

# Students
@app.get("/students", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_students(db, skip=skip, limit=limit)

@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.post("/students", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_email(db, email=student.email)
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db, student)

# Student Progress
@app.get("/students/{student_id}/progress", response_model=List[schemas.StudentProgress])
def read_student_progress(student_id: int, db: Session = Depends(get_db)):
    return crud.get_student_progress(db, student_id)

@app.post("/progress", response_model=schemas.StudentProgress)
def create_progress(progress: schemas.StudentProgressCreate, db: Session = Depends(get_db)):
    return crud.create_student_progress(db, progress)

@app.put("/progress/{progress_id}")
def update_progress(progress_id: int, progress_data: dict, db: Session = Depends(get_db)):
    return crud.update_student_progress(db, progress_id, progress_data)

# Learning Paths
@app.get("/learning-paths", response_model=List[schemas.LearningPath])
def read_learning_paths(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_learning_paths(db, skip=skip, limit=limit)

@app.post("/learning-paths", response_model=schemas.LearningPath)
def create_learning_path(path: schemas.LearningPathCreate, db: Session = Depends(get_db)):
    return crud.create_learning_path(db, path)

# Class Schedules
@app.get("/schedules", response_model=List[schemas.ClassSchedule])
def read_schedules(class_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_class_schedules(db, class_id)

@app.post("/schedules", response_model=schemas.ClassSchedule)
def create_schedule(schedule: schemas.ClassScheduleCreate, db: Session = Depends(get_db)):
    return crud.create_class_schedule(db, schedule)

# AI Recommendations
@app.get("/students/{student_id}/recommendations", response_model=List[schemas.ClassRecommendation])
def get_recommendations(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return crud.get_class_recommendations(db, student_id)

# Dashboard
@app.get("/dashboard/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)

@app.get("/analytics/overview")
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)