from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import crud, models, schemas
from database import SessionLocal, engine
from ai_service import faculty_ai_service
from data_import import faculty_import_service
from pydantic import BaseModel
from profile_models import FacultyProfile, FacultyEvaluation, PerformanceMetric, FacultyGoal, ProfessionalDevelopment
import profile_schemas
from typing import Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Faculty Performance & Research Analytics Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Faculty Performance & Research Analytics Platform API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Faculty Management Endpoints
@app.post("/faculty/", response_model=schemas.Faculty)
def create_faculty(faculty: schemas.FacultyCreate, db: Session = Depends(get_db)):
    db_faculty = crud.get_faculty_by_faculty_id(db, faculty_id=faculty.faculty_id)
    if db_faculty:
        raise HTTPException(status_code=400, detail="Faculty ID already registered")
    return crud.create_faculty(db=db, faculty=faculty)

@app.get("/faculty/", response_model=List[schemas.Faculty])
def read_faculty(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    faculty = crud.get_faculty_list(db, skip=skip, limit=limit)
    return faculty

@app.get("/faculty/{faculty_id}", response_model=schemas.Faculty)
def read_faculty_member(faculty_id: int, db: Session = Depends(get_db)):
    db_faculty = crud.get_faculty(db, faculty_id=faculty_id)
    if db_faculty is None:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    return db_faculty

@app.get("/faculty/{faculty_id}/analytics", response_model=schemas.FacultyPerformanceAnalytics)
def get_faculty_analytics(faculty_id: int, db: Session = Depends(get_db)):
    faculty = crud.get_faculty(db, faculty_id=faculty_id)
    if faculty is None:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    
    # Get comprehensive analytics
    research_metrics = crud.get_faculty_research_metrics(db, faculty_id)
    teaching_metrics = crud.get_faculty_teaching_metrics(db, faculty_id)
    service_metrics = crud.get_faculty_service_metrics(db, faculty_id)
    overall_scores = crud.get_faculty_overall_scores(db, faculty_id)
    recent_achievements = crud.get_faculty_recent_achievements(db, faculty_id)
    
    # Get AI-generated insights
    improvement_areas = crud.get_faculty_insights(db, faculty_id, "weakness")
    recommendations = crud.get_faculty_insights(db, faculty_id, "recommendation")
    
    return schemas.FacultyPerformanceAnalytics(
        faculty=faculty,
        research_metrics=research_metrics,
        teaching_metrics=teaching_metrics,
        service_metrics=service_metrics,
        overall_scores=overall_scores,
        recent_achievements=recent_achievements,
        improvement_areas=improvement_areas,
        recommendations=recommendations
    )

# Research Management Endpoints
@app.post("/research/", response_model=schemas.Research)
def create_research(research: schemas.ResearchCreate, db: Session = Depends(get_db)):
    return crud.create_research(db=db, research=research)

@app.get("/research/faculty/{faculty_id}", response_model=List[schemas.Research])
def read_faculty_research(faculty_id: int, db: Session = Depends(get_db)):
    research = crud.get_faculty_research(db, faculty_id=faculty_id)
    return research

# Teaching Management Endpoints  
@app.post("/teaching/", response_model=schemas.Teaching)
def create_teaching(teaching: schemas.TeachingCreate, db: Session = Depends(get_db)):
    return crud.create_teaching(db=db, teaching=teaching)

@app.get("/teaching/faculty/{faculty_id}", response_model=List[schemas.Teaching])
def read_faculty_teaching(faculty_id: int, db: Session = Depends(get_db)):
    teaching = crud.get_faculty_teaching(db, faculty_id=faculty_id)
    return teaching


# AI Analysis Endpoints
@app.post("/faculty/{faculty_id}/analyze")
def analyze_faculty_performance(faculty_id: int, db: Session = Depends(get_db)):
    faculty = crud.get_faculty(db, faculty_id=faculty_id)
    if faculty is None:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    
    insights = faculty_ai_service.analyze_faculty_performance(db, faculty_id)
    
    # Save insights to database
    saved_insights = []
    for insight in insights:
        saved_insight = crud.create_faculty_insight(db, insight)
        saved_insights.append(saved_insight)
    
    return {"message": f"Generated {len(saved_insights)} insights for faculty member", "insights": saved_insights}

@app.get("/faculty/{faculty_id}/research-predictions")
def get_research_predictions(faculty_id: int, db: Session = Depends(get_db)):
    faculty = crud.get_faculty(db, faculty_id=faculty_id)
    if faculty is None:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    
    predictions = faculty_ai_service.predict_research_impact(db, faculty_id)
    return {"predictions": predictions}

@app.get("/faculty/{faculty_id}/collaboration-opportunities")
def get_collaboration_opportunities(faculty_id: int, db: Session = Depends(get_db)):
    faculty = crud.get_faculty(db, faculty_id=faculty_id)
    if faculty is None:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    
    opportunities = faculty_ai_service.identify_collaboration_opportunities(db, faculty_id)
    return {"opportunities": opportunities}

# Department Analytics Endpoints
@app.get("/analytics/department/{department}")
def get_department_analytics(department: str, db: Session = Depends(get_db)):
    analytics = crud.get_department_analytics(db, department)
    return analytics

@app.get("/analytics/dashboard")
def get_dashboard_analytics(db: Session = Depends(get_db)):
    stats = crud.get_dashboard_stats(db)
    research_overview = crud.get_research_overview(db)
    teaching_overview = crud.get_teaching_overview(db)
    collaboration_network = crud.get_collaboration_network_stats(db)
    top_performers = crud.get_top_performers(db)
    
    return {
        "overview": stats,
        "research_overview": research_overview,
        "teaching_overview": teaching_overview,
        "collaboration_network": collaboration_network,
        "top_performers": top_performers
    }

@app.get("/analytics/research-trends")
def get_research_trends(db: Session = Depends(get_db)):
    trends = crud.get_research_trends_over_time(db)
    domain_analysis = crud.get_research_domain_analysis(db)
    impact_analysis = crud.get_impact_factor_analysis(db)
    
    return {
        "publication_trends": trends,
        "domain_analysis": domain_analysis,
        "impact_analysis": impact_analysis
    }

@app.get("/analytics/teaching-excellence")
def get_teaching_excellence_analytics(db: Session = Depends(get_db)):
    excellence_metrics = crud.get_teaching_excellence_metrics(db)
    innovation_analysis = crud.get_teaching_innovation_analysis(db)
    student_success_correlation = crud.get_student_success_correlation(db)
    
    return {
        "excellence_metrics": excellence_metrics,
        "innovation_analysis": innovation_analysis,
        "student_success_correlation": student_success_correlation
    }

# Data Import Endpoints
class ImportData(BaseModel):
    data: str

@app.post("/import/faculty")
def import_faculty_data(import_data: ImportData, db: Session = Depends(get_db)):
    result = faculty_import_service.import_faculty(db, import_data.data)
    return result

@app.post("/import/research")
def import_research_data(import_data: ImportData, db: Session = Depends(get_db)):
    result = faculty_import_service.import_research(db, import_data.data)
    return result

@app.post("/import/teaching")
def import_teaching_data(import_data: ImportData, db: Session = Depends(get_db)):
    result = faculty_import_service.import_teaching(db, import_data.data)
    return result

# ============================================================================
# FACULTY PROFILING SYSTEM ENDPOINTS
# ============================================================================

# Faculty Profile Management
@app.post("/profiles/", response_model=profile_schemas.FacultyProfile)
def create_faculty_profile(profile: profile_schemas.FacultyProfileCreate, db: Session = Depends(get_db)):
    """Create a new faculty profile"""
    # Check if faculty exists
    faculty = crud.get_faculty(db, faculty_id=profile.faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    
    # Check if profile already exists
    existing_profile = db.query(FacultyProfile).filter(FacultyProfile.faculty_id == profile.faculty_id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists for this faculty member")
    
    # Create profile
    db_profile = FacultyProfile(**profile.dict())
    db_profile.completion_percentage = calculate_profile_completion(profile)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@app.get("/profiles/{faculty_id}", response_model=profile_schemas.FacultyProfile)
def get_faculty_profile(faculty_id: int, db: Session = Depends(get_db)):
    """Get faculty profile by faculty ID"""
    profile = db.query(FacultyProfile).filter(FacultyProfile.faculty_id == faculty_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Faculty profile not found")
    return profile

@app.put("/profiles/{faculty_id}", response_model=profile_schemas.FacultyProfile)
def update_faculty_profile(faculty_id: int, profile_update: profile_schemas.FacultyProfileUpdate, db: Session = Depends(get_db)):
    """Update faculty profile"""
    profile = db.query(FacultyProfile).filter(FacultyProfile.faculty_id == faculty_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Faculty profile not found")
    
    # Update fields
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    # Recalculate completion percentage
    profile.completion_percentage = calculate_profile_completion(profile)
    profile.last_updated = datetime.utcnow()
    
    db.commit()
    db.refresh(profile)
    return profile

@app.get("/profiles/", response_model=List[profile_schemas.FacultyProfile])
def list_faculty_profiles(skip: int = 0, limit: int = 100, public_only: bool = False, db: Session = Depends(get_db)):
    """List all faculty profiles"""
    query = db.query(FacultyProfile)
    if public_only:
        query = query.filter(FacultyProfile.is_public == True)
    
    profiles = query.offset(skip).limit(limit).all()
    return profiles

# Faculty Evaluation Management
@app.post("/evaluations/", response_model=profile_schemas.FacultyEvaluation)
def create_faculty_evaluation(evaluation: profile_schemas.FacultyEvaluationCreate, db: Session = Depends(get_db)):
    """Create a new faculty evaluation"""
    # Check if faculty exists
    faculty = crud.get_faculty(db, faculty_id=evaluation.faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    
    db_evaluation = FacultyEvaluation(**evaluation.dict())
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation

@app.get("/evaluations/faculty/{faculty_id}", response_model=List[profile_schemas.FacultyEvaluation])
def get_faculty_evaluations(faculty_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get evaluations for a faculty member"""
    evaluations = db.query(FacultyEvaluation).filter(
        FacultyEvaluation.faculty_id == faculty_id
    ).order_by(FacultyEvaluation.evaluation_date.desc()).limit(limit).all()
    return evaluations

@app.get("/evaluations/{evaluation_id}", response_model=profile_schemas.FacultyEvaluation)
def get_evaluation(evaluation_id: int, db: Session = Depends(get_db)):
    """Get specific evaluation"""
    evaluation = db.query(FacultyEvaluation).filter(FacultyEvaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation

@app.put("/evaluations/{evaluation_id}", response_model=profile_schemas.FacultyEvaluation)
def update_evaluation(evaluation_id: int, evaluation_update: profile_schemas.FacultyEvaluationCreate, db: Session = Depends(get_db)):
    """Update an evaluation"""
    evaluation = db.query(FacultyEvaluation).filter(FacultyEvaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    update_data = evaluation_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(evaluation, field, value)
    
    db.commit()
    db.refresh(evaluation)
    return evaluation

# Performance Metrics Management
@app.post("/metrics/", response_model=profile_schemas.PerformanceMetric)
def create_performance_metric(metric: profile_schemas.PerformanceMetricCreate, db: Session = Depends(get_db)):
    """Create a new performance metric"""
    db_metric = PerformanceMetric(**metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@app.get("/metrics/faculty/{faculty_id}", response_model=List[profile_schemas.PerformanceMetric])
def get_faculty_metrics(faculty_id: int, category: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    """Get performance metrics for a faculty member"""
    query = db.query(PerformanceMetric).filter(PerformanceMetric.faculty_id == faculty_id)
    
    if category:
        query = query.filter(PerformanceMetric.metric_category == category)
    
    metrics = query.order_by(PerformanceMetric.measurement_date.desc()).limit(limit).all()
    return metrics

# Faculty Goals Management
@app.post("/goals/", response_model=profile_schemas.FacultyGoal)
def create_faculty_goal(goal: profile_schemas.FacultyGoalCreate, db: Session = Depends(get_db)):
    """Create a new faculty goal"""
    db_goal = FacultyGoal(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@app.get("/goals/faculty/{faculty_id}", response_model=List[profile_schemas.FacultyGoal])
def get_faculty_goals(faculty_id: int, status: Optional[str] = None, db: Session = Depends(get_db)):
    """Get goals for a faculty member"""
    query = db.query(FacultyGoal).filter(FacultyGoal.faculty_id == faculty_id)
    
    if status:
        query = query.filter(FacultyGoal.status == status)
    
    goals = query.order_by(FacultyGoal.target_date.asc()).all()
    return goals

@app.put("/goals/{goal_id}", response_model=profile_schemas.FacultyGoal)
def update_faculty_goal(goal_id: int, goal_update: profile_schemas.FacultyGoalUpdate, db: Session = Depends(get_db)):
    """Update a faculty goal"""
    goal = db.query(FacultyGoal).filter(FacultyGoal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    update_data = goal_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(goal, field, value)
    
    goal.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(goal)
    return goal

# Professional Development Management
@app.post("/development/", response_model=profile_schemas.ProfessionalDevelopment)
def create_professional_development(development: profile_schemas.ProfessionalDevelopmentCreate, db: Session = Depends(get_db)):
    """Create a new professional development record"""
    db_development = ProfessionalDevelopment(**development.dict())
    db.add(db_development)
    db.commit()
    db.refresh(db_development)
    return db_development

@app.get("/development/faculty/{faculty_id}", response_model=List[profile_schemas.ProfessionalDevelopment])
def get_faculty_development(faculty_id: int, limit: int = 20, db: Session = Depends(get_db)):
    """Get professional development records for a faculty member"""
    development = db.query(ProfessionalDevelopment).filter(
        ProfessionalDevelopment.faculty_id == faculty_id
    ).order_by(ProfessionalDevelopment.activity_date.desc()).limit(limit).all()
    return development

# Comprehensive Faculty Dashboard
@app.get("/dashboard/faculty/{faculty_id}", response_model=profile_schemas.FacultyDashboard)
def get_faculty_dashboard(faculty_id: int, db: Session = Depends(get_db)):
    """Get comprehensive faculty dashboard with all related data"""
    # Get faculty basic info
    faculty = crud.get_faculty(db, faculty_id=faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty member not found")
    
    # Get profile
    profile = db.query(FacultyProfile).filter(FacultyProfile.faculty_id == faculty_id).first()
    
    # Get recent evaluations
    recent_evaluations = db.query(FacultyEvaluation).filter(
        FacultyEvaluation.faculty_id == faculty_id
    ).order_by(FacultyEvaluation.evaluation_date.desc()).limit(5).all()
    
    # Get performance metrics
    performance_metrics = db.query(PerformanceMetric).filter(
        PerformanceMetric.faculty_id == faculty_id
    ).order_by(PerformanceMetric.measurement_date.desc()).limit(20).all()
    
    # Get active goals
    active_goals = db.query(FacultyGoal).filter(
        FacultyGoal.faculty_id == faculty_id,
        FacultyGoal.status.in_(["not_started", "in_progress"])
    ).order_by(FacultyGoal.target_date.asc()).limit(10).all()
    
    # Get recent development
    recent_development = db.query(ProfessionalDevelopment).filter(
        ProfessionalDevelopment.faculty_id == faculty_id
    ).order_by(ProfessionalDevelopment.activity_date.desc()).limit(10).all()
    
    # Calculate analytics summary
    analytics_summary = calculate_faculty_analytics_summary(db, faculty_id, recent_evaluations, performance_metrics)
    
    # Generate recommendations
    recommendations = generate_faculty_recommendations(profile, recent_evaluations, active_goals)
    
    return profile_schemas.FacultyDashboard(
        faculty=faculty.__dict__,
        profile=profile,
        recent_evaluations=recent_evaluations,
        performance_metrics=performance_metrics,
        active_goals=active_goals,
        recent_development=recent_development,
        analytics_summary=analytics_summary,
        recommendations=recommendations
    )

# Faculty Evaluation Analytics
@app.get("/analytics/evaluations/faculty/{faculty_id}", response_model=profile_schemas.EvaluationAnalytics)
def get_faculty_evaluation_analytics(faculty_id: int, db: Session = Depends(get_db)):
    """Get detailed evaluation analytics for a faculty member"""
    evaluations = db.query(FacultyEvaluation).filter(
        FacultyEvaluation.faculty_id == faculty_id
    ).order_by(FacultyEvaluation.evaluation_date.asc()).all()
    
    if not evaluations:
        raise HTTPException(status_code=404, detail="No evaluations found for faculty member")
    
    # Calculate trends
    evaluation_trends = calculate_evaluation_trends(evaluations)
    performance_comparison = calculate_performance_comparison(db, faculty_id, evaluations)
    strengths_analysis = analyze_strengths_frequency(evaluations)
    improvement_tracking = track_improvement_areas(evaluations)
    
    # Calculate goal completion rate
    completed_goals = db.query(FacultyGoal).filter(
        FacultyGoal.faculty_id == faculty_id,
        FacultyGoal.status == "completed"
    ).count()
    total_goals = db.query(FacultyGoal).filter(FacultyGoal.faculty_id == faculty_id).count()
    goal_completion_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0
    
    # Calculate development impact
    development_impact = calculate_development_impact(db, faculty_id)
    
    return profile_schemas.EvaluationAnalytics(
        faculty_id=faculty_id,
        evaluation_trends=evaluation_trends,
        performance_comparison=performance_comparison,
        strengths_analysis=strengths_analysis,
        improvement_tracking=improvement_tracking,
        goal_completion_rate=goal_completion_rate,
        development_impact=development_impact
    )

# ============================================================================
# HELPER FUNCTIONS FOR PROFILING SYSTEM
# ============================================================================

def calculate_profile_completion(profile) -> float:
    """Calculate profile completion percentage for ESL teachers"""
    total_fields = 40  # Total number of profile fields
    completed_fields = 0
    
    # Check each field for completion
    fields_to_check = [
        'bio', 'teaching_philosophy', 'career_goals', 'classroom_location', 'phone', 
        'email_contact', 'emergency_contact', 'education_history', 'esl_certifications',
        'teaching_licenses', 'years_esl_experience', 'years_total_teaching', 
        'previous_schools', 'grade_levels_taught', 'student_age_groups', 'class_sizes_comfortable',
        'native_language', 'languages_spoken', 'languages_can_teach', 'esl_specializations',
        'student_proficiency_levels', 'curriculum_experience', 'assessment_methods',
        'preferred_teaching_methods', 'technology_skills', 'online_teaching_experience',
        'hybrid_teaching_experience', 'student_support_methods', 'parent_communication_methods',
        'cultural_sensitivity_training', 'special_needs_experience', 'recent_professional_development',
        'short_term_goals', 'long_term_goals', 'desired_training_areas', 'schedule_flexibility',
        'preferred_class_times', 'willing_to_tutor', 'available_for_substituting'
    ]
    
    for field in fields_to_check:
        value = getattr(profile, field, None)
        if value is not None and value != "" and value != []:
            completed_fields += 1
    
    return (completed_fields / total_fields) * 100

def calculate_faculty_analytics_summary(db: Session, faculty_id: int, evaluations, metrics) -> dict:
    """Calculate analytics summary for faculty dashboard"""
    summary = {
        "total_evaluations": len(evaluations),
        "latest_overall_score": None,
        "performance_trend": "stable",
        "metrics_count": len(metrics),
        "evaluation_average": None
    }
    
    if evaluations:
        latest_eval = evaluations[0]
        summary["latest_overall_score"] = latest_eval.overall_performance
        
        # Calculate average scores
        overall_scores = [e.overall_performance for e in evaluations if e.overall_performance]
        if overall_scores:
            summary["evaluation_average"] = sum(overall_scores) / len(overall_scores)
            
            # Determine trend
            if len(overall_scores) > 1:
                recent_avg = sum(overall_scores[:2]) / 2 if len(overall_scores) > 1 else overall_scores[0]
                older_avg = sum(overall_scores[2:]) / len(overall_scores[2:]) if len(overall_scores) > 2 else recent_avg
                
                if recent_avg > older_avg + 0.5:
                    summary["performance_trend"] = "improving"
                elif recent_avg < older_avg - 0.5:
                    summary["performance_trend"] = "declining"
    
    return summary

def generate_faculty_recommendations(profile, evaluations, goals) -> List[str]:
    """Generate personalized recommendations for faculty member"""
    recommendations = []
    
    # Profile completion recommendations
    if profile and profile.completion_percentage < 80:
        recommendations.append("Complete your faculty profile to increase visibility and opportunities")
    
    # Evaluation-based recommendations
    if evaluations:
        latest_eval = evaluations[0]
        
        if latest_eval.classroom_management_skills and latest_eval.classroom_management_skills < 7:
            recommendations.append("Consider professional development in classroom management techniques")
        
        if latest_eval.student_engagement_level and latest_eval.student_engagement_level < 7:
            recommendations.append("Focus on improving student engagement strategies and interactive teaching methods")
        
        if latest_eval.language_instruction_quality and latest_eval.language_instruction_quality < 7:
            recommendations.append("Explore advanced ESL teaching methodologies and language instruction techniques")
        
        if latest_eval.technology_adoption and latest_eval.technology_adoption < 6:
            recommendations.append("Invest in educational technology training to enhance digital teaching skills")
        
        if latest_eval.parent_community_engagement and latest_eval.parent_community_engagement < 6:
            recommendations.append("Strengthen parent communication and community engagement activities")
    
    # Goal-based recommendations
    overdue_goals = [g for g in goals if g.target_date < datetime.utcnow() and g.status != "completed"]
    if overdue_goals:
        recommendations.append(f"Review and update {len(overdue_goals)} overdue goals")
    
    # Default recommendations if none generated
    if not recommendations:
        recommendations = [
            "Continue maintaining excellent ESL teaching performance",
            "Consider setting new professional development goals in language instruction",
            "Explore collaboration opportunities with fellow ESL educators",
            "Stay updated with the latest ESL teaching methodologies and technologies"
        ]
    
    return recommendations

def calculate_evaluation_trends(evaluations) -> dict:
    """Calculate evaluation trends over time for ESL teachers"""
    trends = {
        "teaching_effectiveness_trend": [],
        "student_progress_trend": [],
        "collaboration_trend": [],
        "professional_development_trend": [],
        "overall_trend": []
    }
    
    for eval in evaluations:
        eval_data = {
            "date": eval.evaluation_date.isoformat(),
            "period": eval.evaluation_period
        }
        
        # Calculate average teaching effectiveness
        teaching_scores = [eval.lesson_planning_effectiveness, eval.classroom_management_skills, 
                          eval.student_engagement_level, eval.language_instruction_quality]
        teaching_avg = sum(score for score in teaching_scores if score) / len([s for s in teaching_scores if s]) if any(teaching_scores) else None
        if teaching_avg:
            trends["teaching_effectiveness_trend"].append({**eval_data, "value": teaching_avg})
        
        # Calculate average student progress
        progress_scores = [eval.student_progress_tracking, eval.learning_objectives_achievement, 
                          eval.language_skills_development, eval.student_motivation_improvement]
        progress_avg = sum(score for score in progress_scores if score) / len([s for s in progress_scores if s]) if any(progress_scores) else None
        if progress_avg:
            trends["student_progress_trend"].append({**eval_data, "value": progress_avg})
        
        # Calculate average collaboration
        collab_scores = [eval.teamwork_collaboration, eval.school_activity_participation, 
                        eval.parent_community_engagement, eval.mentoring_support_colleagues]
        collab_avg = sum(score for score in collab_scores if score) / len([s for s in collab_scores if s]) if any(collab_scores) else None
        if collab_avg:
            trends["collaboration_trend"].append({**eval_data, "value": collab_avg})
        
        # Calculate average professional development
        dev_scores = [eval.continuous_learning_commitment, eval.skill_development_progress, 
                     eval.technology_adoption, eval.cultural_competency_development]
        dev_avg = sum(score for score in dev_scores if score) / len([s for s in dev_scores if s]) if any(dev_scores) else None
        if dev_avg:
            trends["professional_development_trend"].append({**eval_data, "value": dev_avg})
        
        if eval.overall_performance:
            trends["overall_trend"].append({**eval_data, "value": eval.overall_performance})
    
    return trends

def calculate_performance_comparison(db: Session, faculty_id: int, evaluations) -> dict:
    """Calculate performance comparison with department averages"""
    if not evaluations:
        return {}
    
    latest_eval = evaluations[0]
    
    # Get department average (simplified - would need actual department data)
    comparison = {
        "classroom_management_vs_dept": latest_eval.classroom_management_skills - 7.5 if latest_eval.classroom_management_skills else 0,
        "student_engagement_vs_dept": latest_eval.student_engagement_level - 7.3 if latest_eval.student_engagement_level else 0,
        "language_instruction_vs_dept": latest_eval.language_instruction_quality - 7.4 if latest_eval.language_instruction_quality else 0,
        "student_progress_vs_dept": latest_eval.student_progress_tracking - 7.1 if latest_eval.student_progress_tracking else 0,
        "collaboration_vs_dept": latest_eval.teamwork_collaboration - 6.8 if latest_eval.teamwork_collaboration else 0,
        "overall_vs_dept": latest_eval.overall_performance - 7.2 if latest_eval.overall_performance else 0
    }
    
    return comparison

def analyze_strengths_frequency(evaluations) -> dict:
    """Analyze frequency of strengths mentioned in evaluations"""
    strengths_count = {}
    
    for eval in evaluations:
        if eval.strengths:
            for strength in eval.strengths:
                strengths_count[strength] = strengths_count.get(strength, 0) + 1
    
    return strengths_count

def track_improvement_areas(evaluations) -> dict:
    """Track improvement areas over time"""
    improvement_tracking = {}
    
    for eval in evaluations:
        if eval.improvement_areas:
            for area in eval.improvement_areas:
                if area not in improvement_tracking:
                    improvement_tracking[area] = []
                
                improvement_tracking[area].append({
                    "date": eval.evaluation_date.isoformat(),
                    "period": eval.evaluation_period,
                    "mentioned": True
                })
    
    return improvement_tracking

def calculate_development_impact(db: Session, faculty_id: int) -> dict:
    """Calculate impact of professional development activities"""
    development_activities = db.query(ProfessionalDevelopment).filter(
        ProfessionalDevelopment.faculty_id == faculty_id
    ).all()
    
    impact = {
        "total_activities": len(development_activities),
        "total_hours": sum(d.duration_hours or 0 for d in development_activities),
        "skills_gained_count": sum(len(d.skills_gained or []) for d in development_activities),
        "certificates_earned": sum(len(d.certificates_earned or []) for d in development_activities)
    }
    
    return impact

