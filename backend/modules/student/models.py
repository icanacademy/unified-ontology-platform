from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    grade_level = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Ontology properties
    properties = Column(JSON)  # Store additional student attributes
    
    # Relationships
    enrollments = relationship("Enrollment", back_populates="student")
    assessments = relationship("Assessment", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    department = Column(String)
    years_experience = Column(Integer)
    
    # Ontology properties
    properties = Column(JSON)
    
    # Relationships
    courses = relationship("Course", back_populates="teacher")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, index=True)
    course_name = Column(String)
    subject = Column(String)
    difficulty_level = Column(Integer)  # 1-5 scale
    credits = Column(Integer)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    
    # Ontology properties
    properties = Column(JSON)
    
    # Relationships
    teacher = relationship("Teacher", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    assessments = relationship("Assessment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active")  # active, completed, dropped
    
    # Ontology properties
    properties = Column(JSON)
    
    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    assessment_type = Column(String)  # quiz, exam, assignment, project
    title = Column(String)
    score = Column(Float)
    max_score = Column(Float)
    assessment_date = Column(DateTime)
    submitted_date = Column(DateTime)
    
    # Ontology properties
    properties = Column(JSON)  # Can store detailed rubric scores, etc.
    
    # Relationships
    student = relationship("Student", back_populates="assessments")
    course = relationship("Course", back_populates="assessments")

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    date = Column(DateTime)
    status = Column(String)  # present, absent, late, excused
    
    # Ontology properties
    properties = Column(JSON)

class Insight(Base):
    __tablename__ = "insights"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    insight_type = Column(String)  # strength, weakness, recommendation
    category = Column(String)  # academic, behavioral, social
    description = Column(Text)
    confidence_score = Column(Float)
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    # AI metadata
    model_used = Column(String)
    data_sources = Column(JSON)  # List of data points used to generate insight