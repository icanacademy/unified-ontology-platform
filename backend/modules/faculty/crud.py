from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from typing import List, Optional, Dict, Any
import models
import schemas
from datetime import datetime, timedelta

# Faculty CRUD operations
def get_faculty(db: Session, faculty_id: int):
    return db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()

def get_faculty_by_faculty_id(db: Session, faculty_id: str):
    return db.query(models.Faculty).filter(models.Faculty.faculty_id == faculty_id).first()

def get_faculty_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Faculty).offset(skip).limit(limit).all()

def create_faculty(db: Session, faculty: schemas.FacultyCreate):
    db_faculty = models.Faculty(**faculty.dict())
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty

# Research CRUD operations
def create_research(db: Session, research: schemas.ResearchCreate):
    db_research = models.Research(**research.dict())
    db.add(db_research)
    db.commit()
    db.refresh(db_research)
    return db_research

def get_faculty_research(db: Session, faculty_id: int):
    return db.query(models.Research).filter(models.Research.faculty_id == faculty_id).all()

# Teaching CRUD operations
def create_teaching(db: Session, teaching: schemas.TeachingCreate):
    db_teaching = models.Teaching(**teaching.dict())
    db.add(db_teaching)
    db.commit()
    db.refresh(db_teaching)
    return db_teaching

def get_faculty_teaching(db: Session, faculty_id: int):
    return db.query(models.Teaching).filter(models.Teaching.faculty_id == faculty_id).all()


# Faculty Insight operations
def create_faculty_insight(db: Session, insight: schemas.FacultyInsightCreate):
    db_insight = models.FacultyInsight(**insight.dict())
    db.add(db_insight)
    db.commit()
    db.refresh(db_insight)
    return db_insight

def get_faculty_insights(db: Session, faculty_id: int, insight_type: Optional[str] = None):
    query = db.query(models.FacultyInsight).filter(models.FacultyInsight.faculty_id == faculty_id)
    if insight_type:
        query = query.filter(models.FacultyInsight.insight_type == insight_type)
    return query.order_by(models.FacultyInsight.generated_at.desc()).all()

# Analytics functions
def get_faculty_research_metrics(db: Session, faculty_id: int) -> Dict[str, float]:
    research_data = db.query(models.Research).filter(models.Research.faculty_id == faculty_id).all()
    
    if not research_data:
        return {
            "total_publications": 0,
            "total_citations": 0,
            "h_index": 0.0,
            "average_impact_factor": 0.0,
            "collaboration_rate": 0.0
        }
    
    total_publications = len(research_data)
    total_citations = sum(r.citation_count for r in research_data if r.citation_count)
    
    # Calculate H-index
    citations = sorted([r.citation_count for r in research_data if r.citation_count], reverse=True)
    h_index = 0
    for i, citation_count in enumerate(citations):
        if citation_count >= i + 1:
            h_index = i + 1
        else:
            break
    
    # Average impact factor
    impact_factors = [r.impact_factor for r in research_data if r.impact_factor]
    avg_impact_factor = sum(impact_factors) / len(impact_factors) if impact_factors else 0.0
    
    # Collaboration rate
    collaborative_papers = len([r for r in research_data if r.co_author_count > 1])
    collaboration_rate = collaborative_papers / total_publications if total_publications > 0 else 0.0
    
    return {
        "total_publications": total_publications,
        "total_citations": total_citations,
        "h_index": float(h_index),
        "average_impact_factor": round(avg_impact_factor, 2),
        "collaboration_rate": round(collaboration_rate, 2)
    }

def get_faculty_teaching_metrics(db: Session, faculty_id: int) -> Dict[str, float]:
    teaching_data = db.query(models.Teaching).filter(models.Teaching.faculty_id == faculty_id).all()
    
    if not teaching_data:
        return {
            "average_student_rating": 0.0,
            "average_completion_rate": 0.0,
            "courses_taught": 0,
            "students_taught": 0,
            "innovation_score": 0.0
        }
    
    avg_rating = sum(t.student_evaluation_score for t in teaching_data) / len(teaching_data)
    avg_completion_rate = sum(t.completion_rate for t in teaching_data) / len(teaching_data)
    courses_taught = len(teaching_data)
    students_taught = sum(t.enrollment_count for t in teaching_data)
    
    innovation_scores = [t.teaching_innovation_score for t in teaching_data if t.teaching_innovation_score]
    avg_innovation = sum(innovation_scores) / len(innovation_scores) if innovation_scores else 0.0
    
    return {
        "average_student_rating": round(avg_rating, 2),
        "average_completion_rate": round(avg_completion_rate, 2),
        "courses_taught": courses_taught,
        "students_taught": students_taught,
        "innovation_score": round(avg_innovation, 2)
    }

def get_faculty_service_metrics(db: Session, faculty_id: int) -> Dict[str, float]:
    service_data = db.query(models.Service).filter(models.Service.faculty_id == faculty_id).all()
    
    if not service_data:
        return {
            "total_service_activities": 0,
            "leadership_roles": 0,
            "monthly_hours": 0.0,
            "visibility_score": 0.0
        }
    
    total_activities = len(service_data)
    leadership_roles = len([s for s in service_data if s.leadership_role])
    
    total_hours = sum(s.time_commitment_hours for s in service_data if s.time_commitment_hours)
    avg_monthly_hours = total_hours / total_activities if total_activities > 0 else 0.0
    
    # Simple visibility scoring
    visibility_scores = {
        'international': 4.0,
        'national': 3.0,
        'university': 2.0,
        'department': 1.0
    }
    
    visibility_score = sum(visibility_scores.get(s.visibility_level, 0) for s in service_data) / total_activities if total_activities > 0 else 0.0
    
    return {
        "total_service_activities": total_activities,
        "leadership_roles": leadership_roles,
        "monthly_hours": round(avg_monthly_hours, 1),
        "visibility_score": round(visibility_score, 2)
    }

def get_faculty_overall_scores(db: Session, faculty_id: int) -> Dict[str, float]:
    research_metrics = get_faculty_research_metrics(db, faculty_id)
    teaching_metrics = get_faculty_teaching_metrics(db, faculty_id)
    service_metrics = get_faculty_service_metrics(db, faculty_id)
    
    # Normalize and combine scores (simplified scoring algorithm)
    research_score = min(100, (research_metrics["h_index"] * 10 + research_metrics["average_impact_factor"] * 20))
    teaching_score = teaching_metrics["average_student_rating"] * 20
    service_score = min(100, service_metrics["visibility_score"] * 25)
    
    overall_score = (research_score * 0.4 + teaching_score * 0.4 + service_score * 0.2)
    
    return {
        "research_score": round(research_score, 1),
        "teaching_score": round(teaching_score, 1),
        "service_score": round(service_score, 1),
        "overall_performance": round(overall_score, 1)
    }

def get_faculty_recent_achievements(db: Session, faculty_id: int) -> List[Dict[str, Any]]:
    # Get recent achievements from the last year
    one_year_ago = datetime.utcnow() - timedelta(days=365)
    
    achievements = []
    
    # Recent publications
    recent_publications = db.query(models.Research).filter(
        models.Research.faculty_id == faculty_id,
        models.Research.publication_date >= one_year_ago
    ).order_by(desc(models.Research.publication_date)).limit(5).all()
    
    for pub in recent_publications:
        achievements.append({
            "type": "publication",
            "title": pub.title,
            "venue": pub.venue,
            "date": pub.publication_date.strftime("%Y-%m-%d"),
            "impact": pub.impact_factor or 0.0
        })
    
    
    return achievements

def get_dashboard_stats(db: Session):
    total_faculty = db.query(models.Faculty).count()
    total_publications = db.query(models.Research).count()
    
    # Average metrics
    avg_h_index = db.query(func.avg(models.Research.h_index_contribution)).scalar() or 0.0
    avg_student_rating = db.query(func.avg(models.Teaching.student_evaluation_score)).scalar() or 0.0
    
    return {
        "total_faculty": total_faculty,
        "total_publications": total_publications,
        "average_h_index": round(avg_h_index, 2),
        "average_teaching_rating": round(avg_student_rating, 2)
    }

def get_research_overview(db: Session):
    # Publication trends by type
    pub_by_type = db.query(
        models.Research.publication_type,
        func.count(models.Research.id).label('count')
    ).group_by(models.Research.publication_type).all()
    
    # Research domain distribution
    domain_dist = db.query(
        models.Research.primary_domain,
        func.count(models.Research.id).label('count')
    ).group_by(models.Research.primary_domain).all()
    
    return {
        "publications_by_type": [{"type": pub_type, "count": count} for pub_type, count in pub_by_type],
        "research_domains": [{"domain": domain, "count": count} for domain, count in domain_dist]
    }

def get_teaching_overview(db: Session):
    # Teaching effectiveness by department
    dept_teaching = db.query(
        models.Faculty.department,
        func.avg(models.Teaching.student_evaluation_score).label('avg_rating')
    ).join(
        models.Teaching, models.Teaching.faculty_id == models.Faculty.id
    ).group_by(models.Faculty.department).all()
    
    return {
        "department_teaching_ratings": [
            {"department": dept, "average_rating": round(float(rating), 2)} 
            for dept, rating in dept_teaching
        ]
    }

def get_collaboration_network_stats(db: Session):
    # Collaboration statistics
    total_collaborations = db.query(models.Collaboration).count()
    international_collab = db.query(models.Collaboration).filter(
        models.Collaboration.collaboration_scope == 'international'
    ).count()
    
    collab_by_type = db.query(
        models.Collaboration.collaboration_type,
        func.count(models.Collaboration.id).label('count')
    ).group_by(models.Collaboration.collaboration_type).all()
    
    return {
        "total_collaborations": total_collaborations,
        "international_percentage": round((international_collab / total_collaborations * 100) if total_collaborations > 0 else 0, 1),
        "collaboration_by_type": [{"type": collab_type, "count": count} for collab_type, count in collab_by_type]
    }

def get_top_performers(db: Session):
    # Get top performers in different categories
    # This would typically involve more complex scoring algorithms
    
    # Top researchers by H-index (simplified)
    top_researchers = db.query(models.Faculty).join(models.Research).group_by(
        models.Faculty.id
    ).order_by(
        desc(func.avg(models.Research.h_index_contribution))
    ).limit(5).all()
    
    # Top teachers by student ratings
    top_teachers = db.query(models.Faculty).join(models.Teaching).group_by(
        models.Faculty.id
    ).order_by(
        desc(func.avg(models.Teaching.student_evaluation_score))
    ).limit(5).all()
    
    return {
        "top_researchers": [
            {
                "name": f"{f.first_name} {f.last_name}",
                "department": f.department,
                "rank": f.academic_rank
            } for f in top_researchers
        ],
        "top_teachers": [
            {
                "name": f"{f.first_name} {f.last_name}",
                "department": f.department,
                "rank": f.academic_rank
            } for f in top_teachers
        ]
    }

def get_department_analytics(db: Session, department: str):
    faculty_in_dept = db.query(models.Faculty).filter(models.Faculty.department == department).all()
    
    if not faculty_in_dept:
        return {"error": "Department not found"}
    
    dept_stats = {
        "department_name": department,
        "faculty_count": len(faculty_in_dept),
        "total_publications": 0,
        "total_grants": 0,
        "average_teaching_rating": 0.0
    }
    
    for faculty in faculty_in_dept:
        research_count = db.query(models.Research).filter(models.Research.faculty_id == faculty.id).count()
        grant_count = db.query(models.Grant).filter(models.Grant.faculty_id == faculty.id).count()
        
        dept_stats["total_publications"] += research_count
        dept_stats["total_grants"] += grant_count
    
    # Average teaching rating for department
    avg_rating = db.query(func.avg(models.Teaching.student_evaluation_score)).join(
        models.Faculty
    ).filter(models.Faculty.department == department).scalar()
    
    dept_stats["average_teaching_rating"] = round(avg_rating or 0.0, 2)
    
    return dept_stats

# Additional analytics functions
def get_research_trends_over_time(db: Session):
    # Placeholder - would implement time-series analysis
    return []

def get_research_domain_analysis(db: Session):
    # Placeholder - would implement domain clustering analysis
    return []

def get_impact_factor_analysis(db: Session):
    # Placeholder - would implement impact factor distribution analysis
    return []

def get_teaching_excellence_metrics(db: Session):
    # Placeholder - would implement teaching excellence scoring
    return {}

def get_teaching_innovation_analysis(db: Session):
    # Placeholder - would implement innovation trend analysis
    return {}

def get_student_success_correlation(db: Session):
    # Placeholder - would implement correlation analysis with student outcomes
    return {}