from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base

class FacultyProfile(Base):
    __tablename__ = "faculty_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    
    # Personal Information
    bio = Column(Text)
    teaching_philosophy = Column(Text)
    career_goals = Column(Text)
    
    # Contact Information
    classroom_location = Column(String)
    phone = Column(String)
    email_contact = Column(String)
    emergency_contact = Column(String)
    
    # Education Background
    education_history = Column(JSON)  # List of degrees/diplomas
    esl_certifications = Column(JSON)  # ESL/TEFL/TESOL certifications
    teaching_licenses = Column(JSON)  # Teaching licenses
    
    # ESL Teaching Experience
    years_esl_experience = Column(Integer)
    years_total_teaching = Column(Integer)
    previous_schools = Column(JSON)  # Schools taught at
    grade_levels_taught = Column(JSON)  # Elementary, Middle, High School, Adult
    student_age_groups = Column(JSON)  # Age ranges taught
    class_sizes_comfortable = Column(String)  # Small (5-15), Medium (16-25), Large (26+)
    
    # Language Skills
    native_language = Column(String)
    languages_spoken = Column(JSON)  # Languages and proficiency levels
    languages_can_teach = Column(JSON)  # Languages they can teach
    
    # ESL Specializations
    esl_specializations = Column(JSON)  # Conversation, Grammar, Writing, Reading, etc.
    student_proficiency_levels = Column(JSON)  # Beginner, Intermediate, Advanced
    curriculum_experience = Column(JSON)  # Curricula they've used
    assessment_methods = Column(JSON)  # Assessment techniques they use
    
    # Teaching Methods & Technology
    preferred_teaching_methods = Column(JSON)  # Interactive, Visual, Auditory, etc.
    technology_skills = Column(JSON)  # Educational technology proficiency
    online_teaching_experience = Column(Boolean, default=False)
    hybrid_teaching_experience = Column(Boolean, default=False)
    
    # Student Support & Engagement
    student_support_methods = Column(JSON)  # Ways they support struggling students
    parent_communication_methods = Column(JSON)  # How they communicate with parents
    cultural_sensitivity_training = Column(JSON)  # Cultural competency training
    special_needs_experience = Column(Boolean, default=False)
    
    # Professional Development & Goals
    recent_professional_development = Column(JSON)  # Recent training/workshops
    short_term_goals = Column(JSON)  # 1-2 year goals
    long_term_goals = Column(JSON)  # 3-5 year goals
    desired_training_areas = Column(JSON)  # Areas wanting to improve
    
    # Availability and Preferences
    schedule_flexibility = Column(String)  # High, Medium, Low
    preferred_class_times = Column(JSON)  # Morning, Afternoon, Evening
    willing_to_tutor = Column(Boolean, default=False)
    available_for_substituting = Column(Boolean, default=False)
    
    # Self-Assessment Scores (1-10 scale)
    classroom_management_confidence = Column(Float)
    lesson_planning_confidence = Column(Float)
    student_engagement_confidence = Column(Float)
    language_assessment_confidence = Column(Float)
    technology_integration_confidence = Column(Float)
    cultural_competency_confidence = Column(Float)
    parent_communication_confidence = Column(Float)
    
    # Profile Status
    completion_percentage = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    is_public = Column(Boolean, default=False)
    
    # Ontology properties
    properties = Column(JSON)

class FacultyEvaluation(Base):
    __tablename__ = "faculty_evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    evaluator_id = Column(Integer, ForeignKey("faculty.id"))  # Who did the evaluation
    evaluation_period = Column(String)  # "2024 Annual", "Spring 2024", etc.
    evaluation_type = Column(String)  # annual, mid-term, promotion, tenure
    
    # Classroom Teaching Evaluation (1-10 scale)
    lesson_planning_effectiveness = Column(Float)
    classroom_management_skills = Column(Float)
    student_engagement_level = Column(Float)
    language_instruction_quality = Column(Float)
    assessment_and_feedback = Column(Float)
    differentiated_instruction = Column(Float)
    teaching_comments = Column(Text)
    
    # Student Progress & Outcomes (1-10 scale)
    student_progress_tracking = Column(Float)
    learning_objectives_achievement = Column(Float)
    language_skills_development = Column(Float)
    student_motivation_improvement = Column(Float)
    retention_and_completion_rates = Column(Float)
    student_outcomes_comments = Column(Text)
    
    # Professional Collaboration & School Contribution (1-10 scale)
    teamwork_collaboration = Column(Float)
    school_activity_participation = Column(Float)
    parent_community_engagement = Column(Float)
    mentoring_support_colleagues = Column(Float)
    school_improvement_contribution = Column(Float)
    collaboration_comments = Column(Text)
    
    # Professional Development & Growth (1-10 scale)
    continuous_learning_commitment = Column(Float)
    skill_development_progress = Column(Float)
    technology_adoption = Column(Float)
    cultural_competency_development = Column(Float)
    professional_development_comments = Column(Text)
    
    # Overall Scores
    overall_performance = Column(Float)
    potential_rating = Column(Float)
    
    # Qualitative Assessment
    strengths = Column(JSON)  # List of strength areas
    improvement_areas = Column(JSON)  # Areas for improvement
    recommendations = Column(JSON)  # Specific recommendations
    goals_next_period = Column(JSON)  # Goals for next evaluation period
    
    # Evaluation Metadata
    evaluation_date = Column(DateTime, default=datetime.utcnow)
    evaluator_notes = Column(Text)
    faculty_self_assessment = Column(JSON)  # Faculty's self-evaluation scores
    
    # Status and Workflow
    status = Column(String, default="draft")  # draft, submitted, reviewed, finalized
    requires_followup = Column(Boolean, default=False)
    followup_date = Column(DateTime)
    
    # Ontology properties
    properties = Column(JSON)

class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    metric_name = Column(String)
    metric_category = Column(String)  # teaching_effectiveness, student_progress, professional_development, collaboration
    
    # Metric Values
    current_value = Column(Float)
    target_value = Column(Float)
    benchmark_value = Column(Float)  # Department/institution average
    
    # Time Period
    measurement_date = Column(DateTime)
    measurement_period = Column(String)  # "2024 Q1", "Fall 2024", etc.
    
    # Context
    metric_description = Column(Text)
    calculation_method = Column(Text)
    data_sources = Column(JSON)
    
    # Trends
    trend_direction = Column(String)  # improving, declining, stable
    percentage_change = Column(Float)  # vs previous period
    
    # Properties
    properties = Column(JSON)

class FacultyGoal(Base):
    __tablename__ = "faculty_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    
    # Goal Information
    goal_title = Column(String)
    goal_description = Column(Text)
    goal_category = Column(String)  # research, teaching, service, career
    priority = Column(String)  # high, medium, low
    
    # Timeline
    target_date = Column(DateTime)
    created_date = Column(DateTime, default=datetime.utcnow)
    
    # Progress Tracking
    status = Column(String, default="not_started")  # not_started, in_progress, completed, cancelled
    progress_percentage = Column(Float, default=0.0)
    
    # Success Metrics
    success_criteria = Column(JSON)  # List of criteria for success
    milestones = Column(JSON)  # List of milestones with dates
    
    # Resources and Support
    required_resources = Column(JSON)
    support_needed = Column(JSON)
    
    # Updates and Notes
    progress_notes = Column(Text)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Properties
    properties = Column(JSON)

class ProfessionalDevelopment(Base):
    __tablename__ = "professional_development"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    
    # Activity Information
    activity_title = Column(String)
    activity_type = Column(String)  # conference, workshop, course, certification, etc.
    activity_description = Column(Text)
    
    # Organization and Details
    organizer = Column(String)
    location = Column(String)
    activity_date = Column(DateTime)
    duration_hours = Column(Float)
    
    # Participation
    participation_type = Column(String)  # attended, presented, organized, etc.
    presentation_title = Column(String)
    
    # Outcomes and Impact
    skills_gained = Column(JSON)
    certificates_earned = Column(JSON)
    networking_contacts = Column(Integer)
    follow_up_actions = Column(JSON)
    
    # Cost and Funding
    cost = Column(Float)
    funding_source = Column(String)
    reimbursement_status = Column(String)
    
    # Documentation
    materials_url = Column(String)
    certificate_url = Column(String)
    reflection_notes = Column(Text)
    
    # Properties
    properties = Column(JSON)