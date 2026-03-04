from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Faculty(Base):
    __tablename__ = "faculty"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    department = Column(String)
    academic_rank = Column(String)  # Assistant Prof, Associate Prof, Full Prof
    tenure_status = Column(String)  # Tenured, Tenure-track, Non-tenure
    hire_date = Column(DateTime)
    years_experience = Column(Integer)
    
    # Ontology properties
    properties = Column(JSON)  # Store additional faculty attributes
    
    # Relationships
    research_works = relationship("Research", back_populates="faculty")
    teaching_assignments = relationship("Teaching", back_populates="faculty")
    collaborations = relationship("Collaboration", back_populates="faculty")
    services = relationship("Service", back_populates="faculty")

class Research(Base):
    __tablename__ = "research"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    title = Column(Text)
    publication_type = Column(String)  # journal, conference, book, chapter
    venue = Column(String)  # Journal/Conference name
    publication_date = Column(DateTime)
    
    # Impact metrics
    citation_count = Column(Integer, default=0)
    impact_factor = Column(Float)
    h_index_contribution = Column(Float)
    
    # Collaboration metrics
    co_author_count = Column(Integer)
    international_collaboration = Column(Boolean, default=False)
    industry_collaboration = Column(Boolean, default=False)
    
    # Research domains
    primary_domain = Column(String)
    secondary_domains = Column(JSON)  # List of additional domains
    
    # Ontology properties
    properties = Column(JSON)
    
    # Relationships
    faculty = relationship("Faculty", back_populates="research_works")

class Teaching(Base):
    __tablename__ = "teaching"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    course_code = Column(String)
    course_name = Column(String)
    semester = Column(String)
    academic_year = Column(String)
    
    # Student metrics
    enrollment_count = Column(Integer)
    completion_rate = Column(Float)
    average_grade = Column(Float)
    
    # Evaluation metrics
    student_evaluation_score = Column(Float)  # 1-5 scale
    peer_evaluation_score = Column(Float)
    teaching_innovation_score = Column(Float)
    
    # Teaching methods
    teaching_methods = Column(JSON)  # List of methods used
    technology_integration = Column(Boolean, default=False)
    active_learning_techniques = Column(JSON)
    
    # Ontology properties
    properties = Column(JSON)
    
    # Relationships
    faculty = relationship("Faculty", back_populates="teaching_assignments")


class Collaboration(Base):
    __tablename__ = "collaborations"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    collaborator_name = Column(String)
    collaborator_institution = Column(String)
    collaboration_type = Column(String)  # research, teaching, service
    
    # Collaboration metrics
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    joint_publications = Column(Integer, default=0)
    joint_grants = Column(Float, default=0.0)  # Total funding
    
    # Geographic scope
    collaboration_scope = Column(String)  # local, national, international
    
    # Ontology properties
    properties = Column(JSON)
    
    # Relationships
    faculty = relationship("Faculty", back_populates="collaborations")

class Service(Base):
    __tablename__ = "service"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    service_type = Column(String)  # editorial, committee, review, administrative
    service_name = Column(String)
    organization = Column(String)
    
    # Time commitment
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    time_commitment_hours = Column(Float)  # Hours per month
    
    # Impact metrics
    leadership_role = Column(Boolean, default=False)
    visibility_level = Column(String)  # department, university, national, international
    
    # Ontology properties
    properties = Column(JSON)
    
    # Relationships
    faculty = relationship("Faculty", back_populates="services")

class FacultyInsight(Base):
    __tablename__ = "faculty_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    insight_type = Column(String)  # strength, weakness, opportunity, recommendation
    category = Column(String)  # research, teaching, service, career
    description = Column(Text)
    confidence_score = Column(Float)
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    # AI metadata
    ai_model_used = Column(String)
    data_sources = Column(JSON)  # List of data points used
    
    # Action items
    priority_level = Column(String)  # high, medium, low
    suggested_actions = Column(JSON)  # List of actionable recommendations

class FacultyPerformanceMetrics(Base):
    __tablename__ = "faculty_performance_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    evaluation_period = Column(String)  # 2023-2024, Spring 2024, etc.
    
    # Research metrics
    research_productivity_score = Column(Float)
    research_impact_score = Column(Float)
    research_collaboration_score = Column(Float)
    
    # Teaching metrics
    teaching_effectiveness_score = Column(Float)
    teaching_innovation_score = Column(Float)
    student_mentorship_score = Column(Float)
    
    # Service metrics
    service_contribution_score = Column(Float)
    leadership_score = Column(Float)
    professional_development_score = Column(Float)
    
    # Overall composite scores
    overall_performance_score = Column(Float)
    career_trajectory_score = Column(Float)
    institutional_value_score = Column(Float)
    
    # Generated insights
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    # Ontology properties for additional metrics
    properties = Column(JSON)