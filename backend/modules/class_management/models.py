from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between classes and prerequisites
class_prerequisites = Table(
    'class_prerequisites',
    Base.metadata,
    Column('class_id', Integer, ForeignKey('classes.id')),
    Column('prerequisite_id', Integer, ForeignKey('classes.id'))
)

# Association table for student enrollments
student_enrollments = Table(
    'student_enrollments',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('class_id', Integer, ForeignKey('classes.id'))
)

class ClassCategory(Base):
    __tablename__ = "class_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    color = Column(String, default="#1976d2")
    
    classes = relationship("Class", back_populates="category")

class Class(Base):
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("class_categories.id"))
    min_grade_level = Column(String)  # e.g., "G1", "G4", "High School"
    max_grade_level = Column(String)
    difficulty_level = Column(Integer)  # 1-5 scale
    duration_weeks = Column(Integer)
    skills_focus = Column(Text)  # JSON string of skills
    learning_objectives = Column(Text)
    materials_needed = Column(Text)
    assessment_methods = Column(Text)
    is_active = Column(Boolean, default=True)
    
    category = relationship("ClassCategory", back_populates="classes")
    enrollments = relationship("Student", secondary=student_enrollments, back_populates="enrolled_classes")
    prerequisites = relationship(
        "Class",
        secondary=class_prerequisites,
        primaryjoin=id == class_prerequisites.c.class_id,
        secondaryjoin=id == class_prerequisites.c.prerequisite_id,
        backref="prerequisite_for"
    )

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    current_grade_level = Column(String)
    english_proficiency_level = Column(String)  # Beginner, Intermediate, Advanced
    join_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    enrolled_classes = relationship("Class", secondary=student_enrollments, back_populates="enrollments")
    progress_records = relationship("StudentProgress", back_populates="student")

class StudentProgress(Base):
    __tablename__ = "student_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    completion_date = Column(DateTime, nullable=True)
    progress_percentage = Column(Float, default=0.0)
    current_level = Column(String)
    performance_score = Column(Float, nullable=True)  # 0-100
    teacher_notes = Column(Text)
    is_completed = Column(Boolean, default=False)
    
    student = relationship("Student", back_populates="progress_records")
    class_ref = relationship("Class")

class LearningPath(Base):
    __tablename__ = "learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    target_grade_level = Column(String)
    target_proficiency = Column(String)
    estimated_duration_months = Column(Integer)
    class_sequence = Column(Text)  # JSON string of ordered class IDs
    is_recommended = Column(Boolean, default=True)
    
class ClassSchedule(Base):
    __tablename__ = "class_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    teacher_name = Column(String)
    day_of_week = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    classroom = Column(String)
    max_students = Column(Integer, default=12)
    current_enrolled = Column(Integer, default=0)
    
    class_ref = relationship("Class")