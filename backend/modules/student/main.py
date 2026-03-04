from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from database import SessionLocal, engine
import assessment_models
from ai_service import ai_service
from data_import import import_service
from assessment_import import assessment_import_service
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)
assessment_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Analytics Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
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
    return {"message": "Student Analytics Platform API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_student_id(db, student_id=student.student_id)
    if db_student:
        raise HTTPException(status_code=400, detail="Student ID already registered")
    return crud.create_student(db=db, student=student)

@app.get("/students/", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.get("/students/{student_id}/analytics", response_model=schemas.StudentAnalytics)
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

@app.post("/teachers/", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return crud.create_teacher(db=db, teacher=teacher)

@app.get("/teachers/", response_model=List[schemas.Teacher])
def read_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teachers = crud.get_teachers(db, skip=skip, limit=limit)
    return teachers

@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db=db, course=course)

@app.get("/courses/", response_model=List[schemas.Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses

@app.post("/assessments/", response_model=schemas.Assessment)
def create_assessment(assessment: schemas.AssessmentCreate, db: Session = Depends(get_db)):
    return crud.create_assessment(db=db, assessment=assessment)

@app.get("/assessments/student/{student_id}", response_model=List[schemas.Assessment])
def read_student_assessments(student_id: int, db: Session = Depends(get_db)):
    assessments = crud.get_student_assessments(db, student_id=student_id)
    return assessments

@app.post("/students/{student_id}/analyze")
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

@app.post("/attendance/", response_model=schemas.Attendance)
def create_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    return crud.create_attendance(db=db, attendance=attendance)

@app.get("/attendance/student/{student_id}")
def read_student_attendance(student_id: int, db: Session = Depends(get_db)):
    attendance = crud.get_student_attendance(db, student_id=student_id)
    return attendance

@app.get("/students/{student_id}/teaching-strategies")
def get_teaching_strategies(student_id: int, weakness_area: str, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    strategies = ai_service.generate_teaching_strategies(db, student_id, weakness_area)
    return {"strategies": strategies}

class ImportData(BaseModel):
    data: str

@app.post("/import/students")
def import_students(import_data: ImportData, db: Session = Depends(get_db)):
    result = import_service.import_students(db, import_data.data)
    return result

@app.post("/import/teachers")
def import_teachers(import_data: ImportData, db: Session = Depends(get_db)):
    result = import_service.import_teachers(db, import_data.data)
    return result

@app.post("/import/courses")
def import_courses(import_data: ImportData, db: Session = Depends(get_db)):
    result = import_service.import_courses(db, import_data.data)
    return result

@app.post("/import/assessments")
def import_assessments(import_data: ImportData, db: Session = Depends(get_db)):
    result = import_service.import_assessments(db, import_data.data)
    return result

@app.post("/import/attendance")
def import_attendance(import_data: ImportData, db: Session = Depends(get_db)):
    result = import_service.import_attendance(db, import_data.data)
    return result

@app.post("/import/level-tests")
def import_level_tests(import_data: ImportData, db: Session = Depends(get_db)):
    result = assessment_import_service.import_level_test(db, import_data.data)
    return result

@app.post("/import/interviews")
def import_interviews(import_data: ImportData, db: Session = Depends(get_db)):
    result = assessment_import_service.import_interview_assessment(db, import_data.data)
    return result

@app.post("/debug/parse-level-test")
def debug_parse_level_test(import_data: ImportData):
    """Debug endpoint to see what gets parsed from level test data"""
    try:
        parsed = assessment_import_service.parse_level_test_data(import_data.data)
        return {"status": "success", "parsed_data": parsed}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.post("/debug/parse-interview")
def debug_parse_interview(import_data: ImportData):
    """Debug endpoint to see what gets parsed from interview data"""
    try:
        parsed = assessment_import_service.parse_interview_data(import_data.data)
        return {"status": "success", "parsed_data": parsed}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/analytics/dashboard")
def get_dashboard_analytics(db: Session = Depends(get_db)):
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

@app.get("/analytics/student/{student_id}/trends")
def get_student_trends(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    trends = crud.get_student_performance_trends(db, student_id)
    assessment_types = crud.get_assessment_type_performance(db, student_id)
    
    return {
        "performance_trends": trends,
        "assessment_type_performance": assessment_types
    }

@app.get("/analytics/assessments/overview")
def get_assessment_analytics_overview(db: Session = Depends(get_db)):
    # Level test statistics
    level_tests = db.query(assessment_models.LevelTest).all()
    interviews = db.query(assessment_models.InterviewAssessment).all()
    
    level_test_stats = {
        "total_level_tests": len(level_tests),
        "average_total_score": sum(test.total_score / test.total_possible * 100 for test in level_tests) / len(level_tests) if level_tests else 0,
        "skill_averages": {}
    }
    
    interview_stats = {
        "total_interviews": len(interviews),
        "average_initial_score": sum(interview.initial_score / interview.total_possible * 100 for interview in interviews) / len(interviews) if interviews else 0,
        "skill_averages": {}
    }
    
    # Calculate skill averages for level tests
    if level_tests:
        skills = ['grammar', 'reading', 'vocabulary', 'listening', 'writing']
        for skill in skills:
            scores = []
            for test in level_tests:
                if skill == 'grammar' and test.grammar_total > 0:
                    scores.append(test.grammar_score / test.grammar_total * 100)
                elif skill == 'reading' and test.reading_total > 0:
                    scores.append(test.reading_score / test.reading_total * 100)
                elif skill == 'vocabulary' and test.vocabulary_total > 0:
                    scores.append(test.vocabulary_score / test.vocabulary_total * 100)
                elif skill == 'listening' and test.listening_total > 0:
                    scores.append(test.listening_score / test.listening_total * 100)
                elif skill == 'writing' and test.writing_score is not None and test.writing_total > 0:
                    scores.append(test.writing_score / test.writing_total * 100)
            
            if scores:
                level_test_stats["skill_averages"][skill] = sum(scores) / len(scores)
    
    # Calculate skill averages for interviews
    if interviews:
        interview_skills = ['pronunciation', 'fluency', 'comprehension', 'insight', 'vocabulary']
        for skill in interview_skills:
            scores = []
            for interview in interviews:
                if skill == 'pronunciation':
                    scores.append(interview.pronunciation_score / 2.0 * 100)
                elif skill == 'fluency':
                    scores.append(interview.fluency_score / 2.0 * 100)
                elif skill == 'comprehension':
                    scores.append(interview.comprehension_score / 2.0 * 100)
                elif skill == 'insight':
                    scores.append(interview.insight_score / 2.0 * 100)
                elif skill == 'vocabulary':
                    scores.append(interview.vocabulary_score / 2.0 * 100)
            
            if scores:
                interview_stats["skill_averages"][skill] = sum(scores) / len(scores)
    
    return {
        "level_tests": level_test_stats,
        "interviews": interview_stats
    }

@app.get("/analytics/students/{student_id}/assessments")
def get_student_assessment_history(student_id: str, db: Session = Depends(get_db)):
    # Get all assessments for student
    level_tests = db.query(assessment_models.LevelTest).filter(
        assessment_models.LevelTest.student_id == student_id
    ).order_by(assessment_models.LevelTest.test_date).all()
    
    interviews = db.query(assessment_models.InterviewAssessment).filter(
        assessment_models.InterviewAssessment.student_id == student_id
    ).order_by(assessment_models.InterviewAssessment.test_date).all()
    
    skill_progressions = db.query(assessment_models.SkillProgression).filter(
        assessment_models.SkillProgression.student_id == student_id
    ).order_by(assessment_models.SkillProgression.test_date).all()
    
    # Format data for charts
    level_test_history = []
    for test in level_tests:
        level_test_history.append({
            "date": test.test_date.strftime("%Y-%m-%d"),
            "total_score": test.total_score / test.total_possible * 100,
            "grammar": test.grammar_score / test.grammar_total * 100,
            "reading": test.reading_score / test.reading_total * 100,
            "vocabulary": test.vocabulary_score / test.vocabulary_total * 100,
            "listening": test.listening_score / test.listening_total * 100,
            "writing": test.writing_score / test.writing_total * 100 if test.writing_score else None
        })
    
    interview_history = []
    for interview in interviews:
        interview_history.append({
            "date": interview.test_date.strftime("%Y-%m-%d"),
            "overall_score": interview.initial_score / interview.total_possible * 100,
            "pronunciation": interview.pronunciation_score / 2.0 * 100,
            "fluency": interview.fluency_score / 2.0 * 100,
            "comprehension": interview.comprehension_score / 2.0 * 100,
            "insight": interview.insight_score / 2.0 * 100,
            "vocabulary": interview.vocabulary_score / 2.0 * 100
        })
    
    # Group skill progressions by skill
    skill_trends = {}
    for progression in skill_progressions:
        if progression.skill_name not in skill_trends:
            skill_trends[progression.skill_name] = []
        skill_trends[progression.skill_name].append({
            "date": progression.test_date.strftime("%Y-%m-%d"),
            "score": progression.percentage,
            "assessment_type": progression.assessment_type
        })
    
    return {
        "level_test_history": level_test_history,
        "interview_history": interview_history,
        "skill_trends": skill_trends,
        "total_assessments": len(level_tests) + len(interviews)
    }

@app.get("/assessment-students")
def get_assessment_students(db: Session = Depends(get_db)):
    """Get list of students from assessment data"""
    # Get students from level tests
    level_test_students = db.query(assessment_models.LevelTest).distinct(assessment_models.LevelTest.student_name).all()
    interview_students = db.query(assessment_models.InterviewAssessment).distinct(assessment_models.InterviewAssessment.student_name).all()
    
    students = []
    seen_names = set()
    
    # Add level test students
    for test in level_test_students:
        if test.student_name not in seen_names:
            # Count total assessments for this student
            level_test_count = db.query(assessment_models.LevelTest).filter(
                assessment_models.LevelTest.student_id == test.student_id
            ).count()
            
            students.append({
                "name": test.student_name,
                "student_id": test.student_id,
                "grade": test.grade,
                "has_level_tests": True,
                "has_interviews": False,
                "latest_test_date": test.test_date.strftime("%Y-%m-%d") if test.test_date else None,
                "total_assessments": level_test_count
            })
            seen_names.add(test.student_name)
    
    # Add interview students
    for interview in interview_students:
        if interview.student_name not in seen_names:
            interview_count = db.query(assessment_models.InterviewAssessment).filter(
                assessment_models.InterviewAssessment.student_id == interview.student_id
            ).count()
            
            students.append({
                "name": interview.student_name,
                "student_id": interview.student_id,
                "grade": interview.level,
                "has_level_tests": False,
                "has_interviews": True,
                "latest_test_date": interview.test_date.strftime("%Y-%m-%d") if interview.test_date else None,
                "total_assessments": interview_count
            })
            seen_names.add(interview.student_name)
        else:
            # Update existing entry to show both types
            for student in students:
                if student["name"] == interview.student_name:
                    student["has_interviews"] = True
                    # Add interview count to total
                    interview_count = db.query(assessment_models.InterviewAssessment).filter(
                        assessment_models.InterviewAssessment.student_id == interview.student_id
                    ).count()
                    student["total_assessments"] = student.get("total_assessments", 0) + interview_count
                    break
    
    return {"students": students, "total": len(students)}