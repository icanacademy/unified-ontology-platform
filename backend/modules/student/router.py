from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine
from . import assessment_models
from .ai_service import ai_service
from .data_import import import_service
from .assessment_import import assessment_import_service
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)
assessment_models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def student_root():
    return {"message": "Student Analytics Platform API"}

@router.get("/health")
async def student_health_check():
    return {"status": "healthy"}

@router.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_student_id(db, student_id=student.student_id)
    if db_student:
        raise HTTPException(status_code=400, detail="Student ID already registered")
    return crud.create_student(db=db, student=student)

@router.get("/students/", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@router.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.get("/students/{student_id}/analytics", response_model=schemas.StudentAnalytics)
def get_student_analytics(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    gpa = crud.get_student_gpa(db, student_id)
    subject_performance = crud.get_student_subject_performance(db, student_id)
    attendance_rate = crud.get_student_attendance_rate(db, student_id)
    strengths = crud.get_student_insights(db, student_id, "strength")
    weaknesses = crud.get_student_insights(db, student_id, "weakness")
    recommendations = crud.get_student_insights(db, student_id, "recommendation")
    
    return schemas.StudentAnalytics(
        student=student,
        overall_gpa=gpa,
        subject_performance=subject_performance,
        attendance_rate=attendance_rate,
        strengths=strengths,
        weaknesses=weaknesses,
        recommendations=recommendations
    )

@router.post("/teachers/", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return crud.create_teacher(db=db, teacher=teacher)

@router.get("/teachers/", response_model=List[schemas.Teacher])
def read_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teachers = crud.get_teachers(db, skip=skip, limit=limit)
    return teachers

@router.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db=db, course=course)

@router.get("/courses/", response_model=List[schemas.Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses

@router.post("/assessments/", response_model=schemas.Assessment)
def create_assessment(assessment: schemas.AssessmentCreate, db: Session = Depends(get_db)):
    return crud.create_assessment(db=db, assessment=assessment)

@router.get("/assessments/student/{student_id}", response_model=List[schemas.Assessment])
def read_student_assessments(student_id: int, db: Session = Depends(get_db)):
    assessments = crud.get_student_assessments(db, student_id=student_id)
    return assessments

@router.post("/students/{student_id}/analyze")
def analyze_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    insights = ai_service.analyze_student_performance(db, student_id)
    
    # Save insights to database
    saved_insights = []
    for insight in insights:
        saved_insight = crud.create_insight(db, insight)
        saved_insights.append(saved_insight)
    
    return {"message": f"Generated {len(saved_insights)} insights for student", "insights": saved_insights}

@router.get("/analytics/dashboard")
def get_student_dashboard_analytics(db: Session = Depends(get_db)):
    stats = crud.get_dashboard_stats(db)
    grade_distribution = crud.get_grade_level_distribution(db)
    subject_performance = crud.get_subject_performance_overview(db)
    course_difficulty = crud.get_course_difficulty_analysis(db)
    at_risk_students = crud.get_at_risk_students(db)
    teacher_effectiveness = crud.get_teacher_effectiveness(db)
    
    return {
        "overview": stats,
        "grade_distribution": grade_distribution,
        "subject_performance": subject_performance,
        "course_difficulty": course_difficulty,
        "at_risk_students": at_risk_students[:10],  # Top 10 most at-risk
        "teacher_effectiveness": teacher_effectiveness
    }

# Data Import Endpoints
class ImportData(BaseModel):
    data: str

@router.post("/import/students")
def import_students(import_data: ImportData, db: Session = Depends(get_db)):
    result = import_service.import_students(db, import_data.data)
    return result

@router.post("/import/teachers")
def import_teachers(import_data: ImportData, db: Session = Depends(get_db)):
    result = import_service.import_teachers(db, import_data.data)
    return result

@router.post("/import/assessments")
def import_assessments(import_data: ImportData, db: Session = Depends(get_db)):
    result = import_service.import_assessments(db, import_data.data)
    return result