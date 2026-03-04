from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from typing import List, Optional
import json
import models
import schemas

# Class Categories
def get_class_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ClassCategory).offset(skip).limit(limit).all()

def create_class_category(db: Session, category: schemas.ClassCategoryCreate):
    db_category = models.ClassCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Classes
def get_classes(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None):
    query = db.query(models.Class)
    if category_id:
        query = query.filter(models.Class.category_id == category_id)
    return query.offset(skip).limit(limit).all()

def get_class(db: Session, class_id: int):
    return db.query(models.Class).filter(models.Class.id == class_id).first()

def create_class(db: Session, class_data: schemas.ClassCreate):
    db_class = models.Class(**class_data.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def update_class(db: Session, class_id: int, class_data: schemas.ClassCreate):
    db.query(models.Class).filter(models.Class.id == class_id).update(class_data.dict())
    db.commit()
    return db.query(models.Class).filter(models.Class.id == class_id).first()

# Students
def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# Student Progress
def get_student_progress(db: Session, student_id: int):
    return db.query(models.StudentProgress).filter(models.StudentProgress.student_id == student_id).all()

def create_student_progress(db: Session, progress: schemas.StudentProgressCreate):
    db_progress = models.StudentProgress(**progress.dict())
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

def update_student_progress(db: Session, progress_id: int, progress_data: dict):
    db.query(models.StudentProgress).filter(models.StudentProgress.id == progress_id).update(progress_data)
    db.commit()
    return db.query(models.StudentProgress).filter(models.StudentProgress.id == progress_id).first()

# Learning Paths
def get_learning_paths(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LearningPath).offset(skip).limit(limit).all()

def create_learning_path(db: Session, path: schemas.LearningPathCreate):
    db_path = models.LearningPath(**path.dict())
    db.add(db_path)
    db.commit()
    db.refresh(db_path)
    return db_path

# Class Schedules
def get_class_schedules(db: Session, class_id: Optional[int] = None):
    query = db.query(models.ClassSchedule)
    if class_id:
        query = query.filter(models.ClassSchedule.class_id == class_id)
    return query.all()

def create_class_schedule(db: Session, schedule: schemas.ClassScheduleCreate):
    db_schedule = models.ClassSchedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

# AI-powered recommendations
def get_class_recommendations(db: Session, student_id: int) -> List[schemas.ClassRecommendation]:
    student = get_student(db, student_id)
    if not student:
        return []
    
    # Get student's current enrolled classes
    enrolled_classes = db.query(models.StudentProgress).filter(
        models.StudentProgress.student_id == student_id,
        models.StudentProgress.is_completed == False
    ).all()
    
    enrolled_class_ids = [p.class_id for p in enrolled_classes]
    
    # Get all available classes
    available_classes = db.query(models.Class).filter(
        models.Class.is_active == True,
        ~models.Class.id.in_(enrolled_class_ids)
    ).all()
    
    recommendations = []
    
    for cls in available_classes:
        match_score = calculate_class_match_score(student, cls)
        reasons = generate_recommendation_reasons(student, cls)
        
        if match_score > 0.3:  # Threshold for recommendations
            recommendations.append(schemas.ClassRecommendation(
                class_id=cls.id,
                class_name=cls.name,
                match_score=match_score,
                reasons=reasons,
                category=cls.category.name if cls.category else "General"
            ))
    
    # Sort by match score
    recommendations.sort(key=lambda x: x.match_score, reverse=True)
    return recommendations[:5]  # Return top 5

def calculate_class_match_score(student: models.Student, cls: models.Class) -> float:
    score = 0.0
    
    # Grade level matching
    if student.current_grade_level in [cls.min_grade_level, cls.max_grade_level]:
        score += 0.4
    
    # Proficiency level matching
    proficiency_mapping = {
        "Beginner": [1, 2],
        "Intermediate": [2, 3, 4],
        "Advanced": [4, 5]
    }
    
    if student.english_proficiency_level in proficiency_mapping:
        if cls.difficulty_level in proficiency_mapping[student.english_proficiency_level]:
            score += 0.4
    
    # Add some randomness for diversity
    score += 0.2
    
    return min(score, 1.0)

def generate_recommendation_reasons(student: models.Student, cls: models.Class) -> List[str]:
    reasons = []
    
    if student.current_grade_level == cls.min_grade_level:
        reasons.append(f"Perfect grade level match ({student.current_grade_level})")
    
    if student.english_proficiency_level == "Beginner" and cls.difficulty_level <= 2:
        reasons.append("Suitable for beginner level")
    elif student.english_proficiency_level == "Advanced" and cls.difficulty_level >= 4:
        reasons.append("Challenging content for advanced learners")
    
    if "writing" in cls.name.lower():
        reasons.append("Develops essential writing skills")
    elif "speaking" in cls.name.lower():
        reasons.append("Improves speaking confidence")
    elif "reading" in cls.name.lower():
        reasons.append("Enhances reading comprehension")
    
    return reasons

# Dashboard statistics
def get_dashboard_stats(db: Session) -> schemas.DashboardStats:
    total_classes = db.query(models.Class).count()
    active_classes = db.query(models.Class).filter(models.Class.is_active == True).count()
    total_students = db.query(models.Student).count()
    total_enrollments = db.query(models.StudentProgress).count()
    
    completed_enrollments = db.query(models.StudentProgress).filter(
        models.StudentProgress.is_completed == True
    ).count()
    
    completion_rate = (completed_enrollments / max(total_enrollments, 1)) * 100
    
    # Popular classes
    popular_classes = db.query(
        models.Class.name,
        func.count(models.StudentProgress.id).label('enrollment_count')
    ).join(
        models.StudentProgress
    ).group_by(
        models.Class.id, models.Class.name
    ).order_by(
        desc('enrollment_count')
    ).limit(5).all()
    
    popular_classes_data = [
        {"name": name, "enrollments": count} 
        for name, count in popular_classes
    ]
    
    return schemas.DashboardStats(
        total_classes=total_classes,
        active_classes=active_classes,
        total_students=total_students,
        total_enrollments=total_enrollments,
        completion_rate=completion_rate,
        popular_classes=popular_classes_data
    )