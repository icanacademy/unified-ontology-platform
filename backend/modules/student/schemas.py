from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class StudentBase(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    email: str
    grade_level: int
    properties: Optional[Dict[str, Any]] = {}

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TeacherBase(BaseModel):
    teacher_id: str
    first_name: str
    last_name: str
    email: str
    department: str
    years_experience: int
    properties: Optional[Dict[str, Any]] = {}

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int
    
    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    course_code: str
    course_name: str
    subject: str
    difficulty_level: int
    credits: int
    teacher_id: int
    properties: Optional[Dict[str, Any]] = {}

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    
    class Config:
        from_attributes = True

class AssessmentBase(BaseModel):
    student_id: int
    course_id: int
    assessment_type: str
    title: str
    score: float
    max_score: float
    assessment_date: datetime
    submitted_date: Optional[datetime] = None
    properties: Optional[Dict[str, Any]] = {}

class AssessmentCreate(AssessmentBase):
    pass

class Assessment(AssessmentBase):
    id: int
    
    class Config:
        from_attributes = True

class InsightBase(BaseModel):
    student_id: int
    insight_type: str
    category: str
    description: str
    confidence_score: float
    model_used: str
    data_sources: List[str]

class InsightCreate(InsightBase):
    pass

class Insight(InsightBase):
    id: int
    generated_at: datetime
    
    class Config:
        from_attributes = True

class AttendanceBase(BaseModel):
    student_id: int
    course_id: int
    date: datetime
    status: str
    properties: Optional[Dict[str, Any]] = {}

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    
    class Config:
        from_attributes = True

class StudentAnalytics(BaseModel):
    student: Student
    overall_gpa: float
    subject_performance: Dict[str, float]
    attendance_rate: float
    strengths: List[Insight]
    weaknesses: List[Insight]
    recommendations: List[Insight]