from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

# Faculty Schemas
class FacultyBase(BaseModel):
    faculty_id: str
    first_name: str
    last_name: str
    email: str
    department: str
    academic_rank: str
    tenure_status: str
    hire_date: datetime
    years_experience: int
    properties: Optional[Dict[str, Any]] = {}

class FacultyCreate(FacultyBase):
    pass

class Faculty(FacultyBase):
    id: int
    
    class Config:
        from_attributes = True

# Research Schemas
class ResearchBase(BaseModel):
    faculty_id: int
    title: str
    publication_type: str
    venue: str
    publication_date: datetime
    citation_count: Optional[int] = 0
    impact_factor: Optional[float] = None
    h_index_contribution: Optional[float] = None
    co_author_count: int
    international_collaboration: Optional[bool] = False
    industry_collaboration: Optional[bool] = False
    primary_domain: str
    secondary_domains: Optional[List[str]] = []
    properties: Optional[Dict[str, Any]] = {}

class ResearchCreate(ResearchBase):
    pass

class Research(ResearchBase):
    id: int
    
    class Config:
        from_attributes = True

# Teaching Schemas
class TeachingBase(BaseModel):
    faculty_id: int
    course_code: str
    course_name: str
    semester: str
    academic_year: str
    enrollment_count: int
    completion_rate: float
    average_grade: float
    student_evaluation_score: float
    peer_evaluation_score: Optional[float] = None
    teaching_innovation_score: Optional[float] = None
    teaching_methods: Optional[List[str]] = []
    technology_integration: Optional[bool] = False
    active_learning_techniques: Optional[List[str]] = []
    properties: Optional[Dict[str, Any]] = {}

class TeachingCreate(TeachingBase):
    pass

class Teaching(TeachingBase):
    id: int
    
    class Config:
        from_attributes = True


# Faculty Insight Schemas
class FacultyInsightBase(BaseModel):
    faculty_id: int
    insight_type: str
    category: str
    description: str
    confidence_score: float
    model_used: str
    data_sources: List[str]
    priority_level: str
    suggested_actions: Optional[List[str]] = []

class FacultyInsightCreate(FacultyInsightBase):
    pass

class FacultyInsight(FacultyInsightBase):
    id: int
    generated_at: datetime
    
    class Config:
        from_attributes = True

# Performance Analytics Schemas
class FacultyPerformanceAnalytics(BaseModel):
    faculty: Faculty
    research_metrics: Dict[str, float]
    teaching_metrics: Dict[str, float]
    service_metrics: Dict[str, float]
    overall_scores: Dict[str, float]
    recent_achievements: List[Dict[str, Any]]
    improvement_areas: List[FacultyInsight]
    recommendations: List[FacultyInsight]

class ResearchImpactAnalytics(BaseModel):
    total_publications: int
    total_citations: int
    h_index: float
    average_impact_factor: float
    collaboration_network_size: int
    research_trajectory: List[Dict[str, Any]]
    impact_predictions: List[Dict[str, Any]]

class TeachingExcellenceAnalytics(BaseModel):
    average_student_rating: float
    course_success_rate: float
    teaching_innovation_index: float
    student_outcome_correlation: float
    teaching_method_effectiveness: Dict[str, float]
    improvement_suggestions: List[str]

class DepartmentAnalytics(BaseModel):
    department_name: str
    faculty_count: int
    research_output: Dict[str, float]
    teaching_quality: Dict[str, float]
    collaboration_index: float
    top_performers: List[Dict[str, Any]]
    department_strengths: List[str]
    improvement_opportunities: List[str]