from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
import models
import schemas
from datetime import datetime, timedelta

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_student_by_student_id(db: Session, student_id: str):
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_teacher(db: Session, teacher_id: int):
    return db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()

def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Teacher).offset(skip).limit(limit).all()

def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = models.Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def create_assessment(db: Session, assessment: schemas.AssessmentCreate):
    db_assessment = models.Assessment(**assessment.dict())
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment

def get_student_assessments(db: Session, student_id: int):
    return db.query(models.Assessment).filter(models.Assessment.student_id == student_id).all()

def get_course_assessments(db: Session, course_id: int):
    return db.query(models.Assessment).filter(models.Assessment.course_id == course_id).all()

def get_student_gpa(db: Session, student_id: int) -> float:
    assessments = db.query(models.Assessment).filter(models.Assessment.student_id == student_id).all()
    if not assessments:
        return 0.0
    
    total_points = sum((a.score / a.max_score) * 4.0 for a in assessments)
    return round(total_points / len(assessments), 2)

def get_student_subject_performance(db: Session, student_id: int):
    result = db.query(
        models.Course.subject,
        func.avg(models.Assessment.score / models.Assessment.max_score * 100).label('avg_score')
    ).join(
        models.Assessment, models.Assessment.course_id == models.Course.id
    ).filter(
        models.Assessment.student_id == student_id
    ).group_by(models.Course.subject).all()
    
    return {subject: round(float(avg_score), 1) for subject, avg_score in result}

def get_student_attendance_rate(db: Session, student_id: int) -> float:
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    total_days = db.query(models.Attendance).filter(
        models.Attendance.student_id == student_id,
        models.Attendance.date >= thirty_days_ago
    ).count()
    
    present_days = db.query(models.Attendance).filter(
        models.Attendance.student_id == student_id,
        models.Attendance.date >= thirty_days_ago,
        models.Attendance.status == 'present'
    ).count()
    
    return round((present_days / total_days * 100) if total_days > 0 else 0.0, 1)

def create_insight(db: Session, insight: schemas.InsightCreate):
    db_insight = models.Insight(**insight.dict())
    db.add(db_insight)
    db.commit()
    db.refresh(db_insight)
    return db_insight

def get_student_insights(db: Session, student_id: int, insight_type: Optional[str] = None):
    query = db.query(models.Insight).filter(models.Insight.student_id == student_id)
    if insight_type:
        query = query.filter(models.Insight.insight_type == insight_type)
    return query.order_by(models.Insight.generated_at.desc()).all()

def create_attendance(db: Session, attendance: schemas.AttendanceCreate):
    db_attendance = models.Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def get_student_attendance(db: Session, student_id: int):
    return db.query(models.Attendance).filter(models.Attendance.student_id == student_id).all()

def get_dashboard_stats(db: Session):
    """Get comprehensive dashboard statistics"""
    total_students = db.query(models.Student).count()
    total_courses = db.query(models.Course).count()
    total_teachers = db.query(models.Teacher).count()
    total_assessments = db.query(models.Assessment).count()
    
    # Average GPA across all students
    all_assessments = db.query(models.Assessment).all()
    if all_assessments:
        total_gpa_points = sum((a.score / a.max_score) * 4.0 for a in all_assessments)
        avg_gpa = round(total_gpa_points / len(all_assessments), 2)
    else:
        avg_gpa = 0.0
    
    # Overall attendance rate
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    total_attendance_records = db.query(models.Attendance).filter(
        models.Attendance.date >= thirty_days_ago
    ).count()
    
    present_records = db.query(models.Attendance).filter(
        models.Attendance.date >= thirty_days_ago,
        models.Attendance.status == 'present'
    ).count()
    
    avg_attendance = round((present_records / total_attendance_records * 100) if total_attendance_records > 0 else 0.0, 1)
    
    return {
        "total_students": total_students,
        "total_courses": total_courses,
        "total_teachers": total_teachers,
        "total_assessments": total_assessments,
        "average_gpa": avg_gpa,
        "average_attendance": avg_attendance
    }

def get_grade_level_distribution(db: Session):
    """Get distribution of students by grade level"""
    result = db.query(
        models.Student.grade_level,
        func.count(models.Student.id).label('count')
    ).group_by(models.Student.grade_level).order_by(models.Student.grade_level).all()
    
    return [{"grade_level": grade, "count": count} for grade, count in result]

def get_subject_performance_overview(db: Session):
    """Get average performance across all subjects"""
    result = db.query(
        models.Course.subject,
        func.avg(models.Assessment.score / models.Assessment.max_score * 100).label('avg_score'),
        func.count(models.Assessment.id).label('assessment_count')
    ).join(
        models.Assessment, models.Assessment.course_id == models.Course.id
    ).group_by(models.Course.subject).all()
    
    return [{
        "subject": subject,
        "average_score": round(float(avg_score), 1),
        "assessment_count": int(assessment_count)
    } for subject, avg_score, assessment_count in result]

def get_student_performance_trends(db: Session, student_id: int):
    """Get performance trends over time for a student"""
    assessments = db.query(models.Assessment, models.Course.subject).join(
        models.Course, models.Assessment.course_id == models.Course.id
    ).filter(
        models.Assessment.student_id == student_id
    ).order_by(models.Assessment.assessment_date).all()
    
    trends = []
    for assessment, subject in assessments:
        percentage = (assessment.score / assessment.max_score) * 100
        trends.append({
            "date": assessment.assessment_date.strftime("%Y-%m-%d"),
            "score": round(percentage, 1),
            "subject": subject,
            "assessment_type": assessment.assessment_type,
            "title": assessment.title
        })
    
    return trends

def get_course_difficulty_analysis(db: Session):
    """Analyze course difficulty vs student performance"""
    result = db.query(
        models.Course.difficulty_level,
        func.avg(models.Assessment.score / models.Assessment.max_score * 100).label('avg_score'),
        func.count(models.Assessment.id).label('assessment_count')
    ).join(
        models.Assessment, models.Assessment.course_id == models.Course.id
    ).group_by(models.Course.difficulty_level).order_by(models.Course.difficulty_level).all()
    
    return [{
        "difficulty_level": difficulty,
        "average_score": round(float(avg_score), 1),
        "assessment_count": int(assessment_count)
    } for difficulty, avg_score, assessment_count in result]

def get_assessment_type_performance(db: Session, student_id: int = None):
    """Get performance by assessment type"""
    query = db.query(
        models.Assessment.assessment_type,
        func.avg(models.Assessment.score / models.Assessment.max_score * 100).label('avg_score'),
        func.count(models.Assessment.id).label('count')
    )
    
    if student_id:
        query = query.filter(models.Assessment.student_id == student_id)
    
    result = query.group_by(models.Assessment.assessment_type).all()
    
    return [{
        "assessment_type": assessment_type,
        "average_score": round(float(avg_score), 1),
        "count": int(count)
    } for assessment_type, avg_score, count in result]

def get_at_risk_students(db: Session, gpa_threshold: float = 2.0, attendance_threshold: float = 75.0):
    """Identify students who may be at risk based on GPA and attendance"""
    students = db.query(models.Student).all()
    at_risk = []
    
    for student in students:
        gpa = get_student_gpa(db, student.id)
        attendance_rate = get_student_attendance_rate(db, student.id)
        
        risk_factors = []
        if gpa < gpa_threshold:
            risk_factors.append(f"Low GPA: {gpa}")
        if attendance_rate < attendance_threshold:
            risk_factors.append(f"Low attendance: {attendance_rate}%")
        
        if risk_factors:
            at_risk.append({
                "student": student,
                "gpa": gpa,
                "attendance_rate": attendance_rate,
                "risk_factors": risk_factors
            })
    
    return sorted(at_risk, key=lambda x: (x["gpa"], x["attendance_rate"]))

def get_teacher_effectiveness(db: Session):
    """Analyze teacher effectiveness based on student performance in their courses"""
    result = db.query(
        models.Teacher.first_name,
        models.Teacher.last_name,
        models.Course.subject,
        func.avg(models.Assessment.score / models.Assessment.max_score * 100).label('avg_score'),
        func.count(models.Assessment.id).label('assessment_count')
    ).join(
        models.Course, models.Course.teacher_id == models.Teacher.id
    ).join(
        models.Assessment, models.Assessment.course_id == models.Course.id
    ).group_by(
        models.Teacher.id, models.Teacher.first_name, models.Teacher.last_name, models.Course.subject
    ).all()
    
    return [{
        "teacher_name": f"{first_name} {last_name}",
        "subject": subject,
        "average_score": round(float(avg_score), 1),
        "assessment_count": int(assessment_count)
    } for first_name, last_name, subject, avg_score, assessment_count in result]