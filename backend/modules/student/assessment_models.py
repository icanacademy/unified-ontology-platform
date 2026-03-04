from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base

class LevelTest(Base):
    __tablename__ = "level_tests"
    
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String)
    student_id = Column(String, index=True)  # ICN-ST-594 format
    grade = Column(String)  # Grade 5, Adult, etc.
    test_level = Column(String)  # LEVEL 3
    test_date = Column(DateTime)
    
    # Skill Scores
    grammar_score = Column(Integer)
    grammar_total = Column(Integer)
    reading_score = Column(Integer)  
    reading_total = Column(Integer)
    vocabulary_score = Column(Integer)
    vocabulary_total = Column(Integer)
    listening_score = Column(Integer)
    listening_total = Column(Integer)
    writing_score = Column(Integer, nullable=True)
    writing_total = Column(Integer)
    
    total_score = Column(Integer)
    total_possible = Column(Integer)
    
    # AI Analysis
    ai_recommendation = Column(Text)
    
    # Writing Assessment
    writing_response = Column(Text)
    writing_analysis = Column(Text)
    
    # Detailed breakdown
    strengths = Column(JSON)  # Store detailed strengths analysis
    weaknesses = Column(JSON)  # Store detailed weaknesses analysis
    
    created_at = Column(DateTime, default=datetime.utcnow)

class InterviewAssessment(Base):
    __tablename__ = "interview_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String)
    student_id = Column(String, index=True)  # ICN-ST-594 format
    age = Column(Integer)
    level = Column(String)  # Adult, Grade 5, etc.
    test_date = Column(DateTime)
    interviewer = Column(String)
    
    # Overall Scores
    initial_score = Column(Float)
    final_score = Column(Float, nullable=True)
    total_possible = Column(Float, default=20.0)
    
    # Detailed Criteria Scores (0-2 scale typically)
    pronunciation_score = Column(Float)
    fluency_score = Column(Float)  
    comprehension_score = Column(Float)
    insight_score = Column(Float)
    vocabulary_score = Column(Float)
    
    # Question-specific scores
    question_scores = Column(JSON)  # Store N6, D7, E8, A2, P9 scores
    
    # Rhetoric Evaluation
    rhetoric_clarity = Column(Float)
    rhetoric_evidence = Column(Float)
    rhetoric_articulation = Column(Float)
    rhetoric_techniques = Column(Float)
    rhetoric_impact = Column(Float)
    rhetoric_total = Column(Float)
    
    # Knowledge Level (1-3 scale)
    knowledge_level = Column(Integer)
    
    # Narrative and Descriptive Levels
    narrative_level = Column(Float)
    descriptive_level = Column(Float)
    
    # Analysis and feedback
    analysis_text = Column(Text)
    improvement_areas = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class SkillProgression(Base):
    __tablename__ = "skill_progressions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    skill_name = Column(String)  # grammar, reading, vocabulary, etc.
    score = Column(Float)
    max_score = Column(Float)
    percentage = Column(Float)
    assessment_type = Column(String)  # level_test, interview
    assessment_id = Column(Integer)  # Reference to specific assessment
    test_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class StudentProgress(Base):
    __tablename__ = "student_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    student_name = Column(String)
    
    # Latest assessment info
    latest_level_test_id = Column(Integer, nullable=True)
    latest_interview_id = Column(Integer, nullable=True)
    latest_test_date = Column(DateTime)
    
    # Progress metrics
    total_assessments = Column(Integer, default=0)
    average_improvement = Column(Float, default=0.0)
    
    # Current skill levels (latest scores)
    current_grammar = Column(Float, nullable=True)
    current_reading = Column(Float, nullable=True)
    current_vocabulary = Column(Float, nullable=True)
    current_listening = Column(Float, nullable=True)
    current_writing = Column(Float, nullable=True)
    current_speaking = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)