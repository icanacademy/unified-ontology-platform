from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

# Faculty Profile Schemas
class FacultyProfileBase(BaseModel):
    faculty_id: int
    bio: Optional[str] = None
    teaching_philosophy: Optional[str] = None
    career_goals: Optional[str] = None
    
    # Contact Information
    classroom_location: Optional[str] = None
    phone: Optional[str] = None
    email_contact: Optional[str] = None
    emergency_contact: Optional[str] = None
    
    # Education & Certifications
    education_history: Optional[List[Dict[str, Any]]] = []
    esl_certifications: Optional[List[Dict[str, Any]]] = []
    teaching_licenses: Optional[List[Dict[str, Any]]] = []
    
    # ESL Teaching Experience
    years_esl_experience: Optional[int] = None
    years_total_teaching: Optional[int] = None
    previous_schools: Optional[List[Dict[str, Any]]] = []
    grade_levels_taught: Optional[List[str]] = []
    student_age_groups: Optional[List[str]] = []
    class_sizes_comfortable: Optional[str] = None
    
    # Language Skills
    native_language: Optional[str] = None
    languages_spoken: Optional[List[Dict[str, Any]]] = []
    languages_can_teach: Optional[List[str]] = []
    
    # ESL Specializations
    esl_specializations: Optional[List[str]] = []
    student_proficiency_levels: Optional[List[str]] = []
    curriculum_experience: Optional[List[str]] = []
    assessment_methods: Optional[List[str]] = []
    
    # Teaching Methods & Technology
    preferred_teaching_methods: Optional[List[str]] = []
    technology_skills: Optional[List[str]] = []
    online_teaching_experience: Optional[bool] = False
    hybrid_teaching_experience: Optional[bool] = False
    
    # Student Support & Engagement
    student_support_methods: Optional[List[str]] = []
    parent_communication_methods: Optional[List[str]] = []
    cultural_sensitivity_training: Optional[List[Dict[str, Any]]] = []
    special_needs_experience: Optional[bool] = False
    
    # Professional Development & Goals
    recent_professional_development: Optional[List[Dict[str, Any]]] = []
    short_term_goals: Optional[List[str]] = []
    long_term_goals: Optional[List[str]] = []
    desired_training_areas: Optional[List[str]] = []
    
    # Availability and Preferences
    schedule_flexibility: Optional[str] = None
    preferred_class_times: Optional[List[str]] = []
    willing_to_tutor: Optional[bool] = False
    available_for_substituting: Optional[bool] = False
    
    # Self-Assessment Scores (1-10 scale)
    classroom_management_confidence: Optional[float] = None
    lesson_planning_confidence: Optional[float] = None
    student_engagement_confidence: Optional[float] = None
    language_assessment_confidence: Optional[float] = None
    technology_integration_confidence: Optional[float] = None
    cultural_competency_confidence: Optional[float] = None
    parent_communication_confidence: Optional[float] = None
    
    is_public: Optional[bool] = False
    properties: Optional[Dict[str, Any]] = {}

class FacultyProfileCreate(FacultyProfileBase):
    pass

class FacultyProfileUpdate(BaseModel):
    bio: Optional[str] = None
    teaching_philosophy: Optional[str] = None
    career_goals: Optional[str] = None
    classroom_location: Optional[str] = None
    phone: Optional[str] = None
    email_contact: Optional[str] = None
    emergency_contact: Optional[str] = None
    education_history: Optional[List[Dict[str, Any]]] = None
    esl_certifications: Optional[List[Dict[str, Any]]] = None
    teaching_licenses: Optional[List[Dict[str, Any]]] = None
    years_esl_experience: Optional[int] = None
    years_total_teaching: Optional[int] = None
    previous_schools: Optional[List[Dict[str, Any]]] = None
    grade_levels_taught: Optional[List[str]] = None
    student_age_groups: Optional[List[str]] = None
    class_sizes_comfortable: Optional[str] = None
    native_language: Optional[str] = None
    languages_spoken: Optional[List[Dict[str, Any]]] = None
    languages_can_teach: Optional[List[str]] = None
    esl_specializations: Optional[List[str]] = None
    student_proficiency_levels: Optional[List[str]] = None
    curriculum_experience: Optional[List[str]] = None
    assessment_methods: Optional[List[str]] = None
    preferred_teaching_methods: Optional[List[str]] = None
    technology_skills: Optional[List[str]] = None
    online_teaching_experience: Optional[bool] = None
    hybrid_teaching_experience: Optional[bool] = None
    student_support_methods: Optional[List[str]] = None
    parent_communication_methods: Optional[List[str]] = None
    cultural_sensitivity_training: Optional[List[Dict[str, Any]]] = None
    special_needs_experience: Optional[bool] = None
    recent_professional_development: Optional[List[Dict[str, Any]]] = None
    short_term_goals: Optional[List[str]] = None
    long_term_goals: Optional[List[str]] = None
    desired_training_areas: Optional[List[str]] = None
    schedule_flexibility: Optional[str] = None
    preferred_class_times: Optional[List[str]] = None
    willing_to_tutor: Optional[bool] = None
    available_for_substituting: Optional[bool] = None
    classroom_management_confidence: Optional[float] = None
    lesson_planning_confidence: Optional[float] = None
    student_engagement_confidence: Optional[float] = None
    language_assessment_confidence: Optional[float] = None
    technology_integration_confidence: Optional[float] = None
    cultural_competency_confidence: Optional[float] = None
    parent_communication_confidence: Optional[float] = None
    is_public: Optional[bool] = None

class FacultyProfile(FacultyProfileBase):
    id: int
    completion_percentage: float
    last_updated: datetime
    
    class Config:
        from_attributes = True

# Faculty Evaluation Schemas
class FacultyEvaluationBase(BaseModel):
    faculty_id: int
    evaluator_id: Optional[int] = None
    evaluation_period: str
    evaluation_type: str
    # Classroom Teaching Evaluation (1-10 scale)
    lesson_planning_effectiveness: Optional[float] = None
    classroom_management_skills: Optional[float] = None
    student_engagement_level: Optional[float] = None
    language_instruction_quality: Optional[float] = None
    assessment_and_feedback: Optional[float] = None
    differentiated_instruction: Optional[float] = None
    teaching_comments: Optional[str] = None
    
    # Student Progress & Outcomes (1-10 scale)
    student_progress_tracking: Optional[float] = None
    learning_objectives_achievement: Optional[float] = None
    language_skills_development: Optional[float] = None
    student_motivation_improvement: Optional[float] = None
    retention_and_completion_rates: Optional[float] = None
    student_outcomes_comments: Optional[str] = None
    
    # Professional Collaboration & School Contribution (1-10 scale)
    teamwork_collaboration: Optional[float] = None
    school_activity_participation: Optional[float] = None
    parent_community_engagement: Optional[float] = None
    mentoring_support_colleagues: Optional[float] = None
    school_improvement_contribution: Optional[float] = None
    collaboration_comments: Optional[str] = None
    
    # Professional Development & Growth (1-10 scale)
    continuous_learning_commitment: Optional[float] = None
    skill_development_progress: Optional[float] = None
    technology_adoption: Optional[float] = None
    cultural_competency_development: Optional[float] = None
    professional_development_comments: Optional[str] = None
    overall_performance: Optional[float] = None
    potential_rating: Optional[float] = None
    strengths: Optional[List[str]] = []
    improvement_areas: Optional[List[str]] = []
    recommendations: Optional[List[str]] = []
    goals_next_period: Optional[List[str]] = []
    evaluator_notes: Optional[str] = None
    faculty_self_assessment: Optional[Dict[str, float]] = {}
    status: Optional[str] = "draft"
    requires_followup: Optional[bool] = False
    followup_date: Optional[datetime] = None
    properties: Optional[Dict[str, Any]] = {}

class FacultyEvaluationCreate(FacultyEvaluationBase):
    pass

class FacultyEvaluation(FacultyEvaluationBase):
    id: int
    evaluation_date: datetime
    
    class Config:
        from_attributes = True

# Performance Metric Schemas
class PerformanceMetricBase(BaseModel):
    faculty_id: int
    metric_name: str
    metric_category: str
    current_value: float
    target_value: Optional[float] = None
    benchmark_value: Optional[float] = None
    measurement_period: str
    metric_description: Optional[str] = None
    calculation_method: Optional[str] = None
    data_sources: Optional[List[str]] = []
    trend_direction: Optional[str] = None
    percentage_change: Optional[float] = None
    properties: Optional[Dict[str, Any]] = {}

class PerformanceMetricCreate(PerformanceMetricBase):
    pass

class PerformanceMetric(PerformanceMetricBase):
    id: int
    measurement_date: datetime
    
    class Config:
        from_attributes = True

# Faculty Goal Schemas
class FacultyGoalBase(BaseModel):
    faculty_id: int
    goal_title: str
    goal_description: str
    goal_category: str
    priority: str
    target_date: datetime
    status: Optional[str] = "not_started"
    progress_percentage: Optional[float] = 0.0
    success_criteria: Optional[List[str]] = []
    milestones: Optional[List[Dict[str, Any]]] = []
    required_resources: Optional[List[str]] = []
    support_needed: Optional[List[str]] = []
    progress_notes: Optional[str] = None
    properties: Optional[Dict[str, Any]] = {}

class FacultyGoalCreate(FacultyGoalBase):
    pass

class FacultyGoalUpdate(BaseModel):
    goal_title: Optional[str] = None
    goal_description: Optional[str] = None
    goal_category: Optional[str] = None
    priority: Optional[str] = None
    target_date: Optional[datetime] = None
    status: Optional[str] = None
    progress_percentage: Optional[float] = None
    success_criteria: Optional[List[str]] = None
    milestones: Optional[List[Dict[str, Any]]] = None
    required_resources: Optional[List[str]] = None
    support_needed: Optional[List[str]] = None
    progress_notes: Optional[str] = None

class FacultyGoal(FacultyGoalBase):
    id: int
    created_date: datetime
    last_updated: datetime
    
    class Config:
        from_attributes = True

# Professional Development Schemas
class ProfessionalDevelopmentBase(BaseModel):
    faculty_id: int
    activity_title: str
    activity_type: str
    activity_description: Optional[str] = None
    organizer: Optional[str] = None
    location: Optional[str] = None
    activity_date: datetime
    duration_hours: Optional[float] = None
    participation_type: Optional[str] = None
    presentation_title: Optional[str] = None
    skills_gained: Optional[List[str]] = []
    certificates_earned: Optional[List[str]] = []
    networking_contacts: Optional[int] = None
    follow_up_actions: Optional[List[str]] = []
    cost: Optional[float] = None
    funding_source: Optional[str] = None
    reimbursement_status: Optional[str] = None
    materials_url: Optional[str] = None
    certificate_url: Optional[str] = None
    reflection_notes: Optional[str] = None
    properties: Optional[Dict[str, Any]] = {}

class ProfessionalDevelopmentCreate(ProfessionalDevelopmentBase):
    pass

class ProfessionalDevelopment(ProfessionalDevelopmentBase):
    id: int
    
    class Config:
        from_attributes = True

# Comprehensive Faculty Dashboard Schema
class FacultyDashboard(BaseModel):
    faculty: dict
    profile: Optional[FacultyProfile] = None
    recent_evaluations: List[FacultyEvaluation] = []
    performance_metrics: List[PerformanceMetric] = []
    active_goals: List[FacultyGoal] = []
    recent_development: List[ProfessionalDevelopment] = []
    analytics_summary: Dict[str, Any] = {}
    recommendations: List[str] = []

# Evaluation Analytics Schema
class EvaluationAnalytics(BaseModel):
    faculty_id: int
    evaluation_trends: Dict[str, List[Dict[str, Any]]]
    performance_comparison: Dict[str, float]
    strengths_analysis: Dict[str, int]
    improvement_tracking: Dict[str, List[Dict[str, Any]]]
    goal_completion_rate: float
    development_impact: Dict[str, float]