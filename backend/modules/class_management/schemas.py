from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class ClassCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: str = "#1976d2"

class ClassCategoryCreate(ClassCategoryBase):
    pass

class ClassCategory(ClassCategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class ClassBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    min_grade_level: str
    max_grade_level: Optional[str] = None
    difficulty_level: int
    duration_weeks: Optional[int] = None
    skills_focus: Optional[str] = None
    learning_objectives: Optional[str] = None
    materials_needed: Optional[str] = None
    assessment_methods: Optional[str] = None
    is_active: bool = True

class ClassCreate(ClassBase):
    pass

class Class(ClassBase):
    id: int
    category: Optional[ClassCategory] = None
    
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    name: str
    email: str
    current_grade_level: str
    english_proficiency_level: str
    notes: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    join_date: datetime
    
    class Config:
        from_attributes = True

class StudentProgressBase(BaseModel):
    student_id: int
    class_id: int
    progress_percentage: float = 0.0
    current_level: Optional[str] = None
    performance_score: Optional[float] = None
    teacher_notes: Optional[str] = None
    is_completed: bool = False

class StudentProgressCreate(StudentProgressBase):
    pass

class StudentProgress(StudentProgressBase):
    id: int
    enrollment_date: datetime
    completion_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class LearningPathBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_grade_level: str
    target_proficiency: str
    estimated_duration_months: Optional[int] = None
    class_sequence: Optional[str] = None
    is_recommended: bool = True

class LearningPathCreate(LearningPathBase):
    pass

class LearningPath(LearningPathBase):
    id: int
    
    class Config:
        from_attributes = True

class ClassScheduleBase(BaseModel):
    class_id: int
    teacher_name: str
    day_of_week: str
    start_time: str
    end_time: str
    classroom: Optional[str] = None
    max_students: int = 12
    current_enrolled: int = 0

class ClassScheduleCreate(ClassScheduleBase):
    pass

class ClassSchedule(ClassScheduleBase):
    id: int
    
    class Config:
        from_attributes = True

class ClassRecommendation(BaseModel):
    class_id: int
    class_name: str
    match_score: float
    reasons: List[str]
    category: str

class DashboardStats(BaseModel):
    total_classes: int
    active_classes: int
    total_students: int
    total_enrollments: int
    completion_rate: float
    popular_classes: List[dict]