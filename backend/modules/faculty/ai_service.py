import ollama
import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import crud
import schemas
import os

class FacultyAIAnalysisService:
    def __init__(self, model_name: str = "llama3.1"):
        self.model_name = model_name
        self.client = ollama.Client(host=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    
    def analyze_faculty_performance(self, db: Session, faculty_id: int) -> List[schemas.FacultyInsightCreate]:
        faculty = crud.get_faculty(db, faculty_id)
        if not faculty:
            return []
        
        # Gather comprehensive faculty data
        research_metrics = crud.get_faculty_research_metrics(db, faculty_id)
        teaching_metrics = crud.get_faculty_teaching_metrics(db, faculty_id)
        service_metrics = crud.get_faculty_service_metrics(db, faculty_id)
        overall_scores = crud.get_faculty_overall_scores(db, faculty_id)
        recent_achievements = crud.get_faculty_recent_achievements(db, faculty_id)
        
        faculty_data = {
            "faculty_info": {
                "name": f"{faculty.first_name} {faculty.last_name}",
                "department": faculty.department,
                "academic_rank": faculty.academic_rank,
                "tenure_status": faculty.tenure_status,
                "years_experience": faculty.years_experience
            },
            "research_metrics": research_metrics,
            "teaching_metrics": teaching_metrics,
            "service_metrics": service_metrics,
            "overall_scores": overall_scores,
            "recent_achievements": recent_achievements[:5]  # Last 5 achievements
        }
        
        prompt = f"""
        Analyze this faculty member's comprehensive performance data and provide insights:
        
        Faculty Data: {json.dumps(faculty_data, indent=2, default=str)}
        
        Please provide:
        1. 2-3 key research strengths with confidence scores (0.0-1.0)
        2. 2-3 key teaching strengths with confidence scores (0.0-1.0)
        3. 2-3 areas for improvement with confidence scores (0.0-1.0)
        4. 3-4 specific, actionable recommendations for career advancement
        5. 1-2 collaboration opportunities based on research profile
        
        Format your response as JSON with this structure:
        {{
            "research_strengths": [
                {{"description": "strength description", "category": "research", "confidence": 0.85, "priority": "medium"}}
            ],
            "teaching_strengths": [
                {{"description": "teaching strength", "category": "teaching", "confidence": 0.75, "priority": "high"}}
            ],
            "improvement_areas": [
                {{"description": "improvement area", "category": "research|teaching|service", "confidence": 0.80, "priority": "high"}}
            ],
            "recommendations": [
                {{"description": "specific recommendation", "category": "career", "confidence": 0.90, "priority": "high", "actions": ["action1", "action2"]}}
            ],
            "opportunities": [
                {{"description": "collaboration opportunity", "category": "collaboration", "confidence": 0.85, "priority": "medium"}}
            ]
        }}
        
        Be specific and actionable in your recommendations. Consider career stage and institutional context.
        """
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            
            analysis = json.loads(response['message']['content'])
            insights = []
            
            # Process research strengths
            for strength in analysis.get('research_strengths', []):
                insights.append(schemas.FacultyInsightCreate(
                    faculty_id=faculty_id,
                    insight_type="strength",
                    category=strength.get('category', 'research'),
                    description=strength['description'],
                    confidence_score=strength.get('confidence', 0.8),
                    model_used=self.model_name,
                    data_sources=["research_metrics", "publications", "citations", "h_index"],
                    priority_level=strength.get('priority', 'medium'),
                    suggested_actions=[]
                ))
            
            # Process teaching strengths
            for strength in analysis.get('teaching_strengths', []):
                insights.append(schemas.FacultyInsightCreate(
                    faculty_id=faculty_id,
                    insight_type="strength",
                    category=strength.get('category', 'teaching'),
                    description=strength['description'],
                    confidence_score=strength.get('confidence', 0.8),
                    model_used=self.model_name,
                    data_sources=["teaching_metrics", "student_evaluations", "course_performance"],
                    priority_level=strength.get('priority', 'medium'),
                    suggested_actions=[]
                ))
            
            # Process improvement areas
            for improvement in analysis.get('improvement_areas', []):
                insights.append(schemas.FacultyInsightCreate(
                    faculty_id=faculty_id,
                    insight_type="weakness",
                    category=improvement.get('category', 'general'),
                    description=improvement['description'],
                    confidence_score=improvement.get('confidence', 0.8),
                    model_used=self.model_name,
                    data_sources=["comprehensive_metrics", "performance_analysis"],
                    priority_level=improvement.get('priority', 'medium'),
                    suggested_actions=[]
                ))
            
            # Process recommendations
            for recommendation in analysis.get('recommendations', []):
                insights.append(schemas.FacultyInsightCreate(
                    faculty_id=faculty_id,
                    insight_type="recommendation",
                    category=recommendation.get('category', 'career'),
                    description=recommendation['description'],
                    confidence_score=recommendation.get('confidence', 0.8),
                    model_used=self.model_name,
                    data_sources=["career_trajectory", "performance_metrics", "institutional_context"],
                    priority_level=recommendation.get('priority', 'medium'),
                    suggested_actions=recommendation.get('actions', [])
                ))
            
            # Process opportunities
            for opportunity in analysis.get('opportunities', []):
                insights.append(schemas.FacultyInsightCreate(
                    faculty_id=faculty_id,
                    insight_type="opportunity",
                    category=opportunity.get('category', 'collaboration'),
                    description=opportunity['description'],
                    confidence_score=opportunity.get('confidence', 0.8),
                    model_used=self.model_name,
                    data_sources=["research_profile", "collaboration_network", "expertise_analysis"],
                    priority_level=opportunity.get('priority', 'medium'),
                    suggested_actions=[]
                ))
            
            return insights
            
        except Exception as e:
            print(f"Error in faculty AI analysis: {e}")
            return []
    
    def predict_research_impact(self, db: Session, faculty_id: int) -> Dict[str, Any]:
        faculty = crud.get_faculty(db, faculty_id)
        if not faculty:
            return {}
        
        research_metrics = crud.get_faculty_research_metrics(db, faculty_id)
        research_works = crud.get_faculty_research(db, faculty_id)
        
        prompt = f"""
        Based on this faculty member's research profile, predict their future research impact:
        
        Research Metrics: {json.dumps(research_metrics)}
        Recent Publications: {len(research_works)} publications
        
        Provide predictions for:
        1. Expected citation growth over next 2 years
        2. Likelihood of high-impact publication (>90th percentile) in next year
        3. Recommended research directions for maximum impact
        4. Collaboration strategies for impact enhancement
        
        Format as JSON with numerical predictions and confidence intervals.
        """
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {"predictions": response['message']['content']}
            
        except Exception as e:
            print(f"Error in research impact prediction: {e}")
            return {"error": "Unable to generate predictions at this time."}
    
    def identify_collaboration_opportunities(self, db: Session, faculty_id: int) -> List[Dict[str, Any]]:
        faculty = crud.get_faculty(db, faculty_id)
        if not faculty:
            return []
        
        research_works = crud.get_faculty_research(db, faculty_id)
        
        # Get research domains and current collaborations
        domains = list(set([r.primary_domain for r in research_works]))
        
        prompt = f"""
        Based on this faculty member's research profile, identify collaboration opportunities:
        
        Faculty: {faculty.first_name} {faculty.last_name}
        Department: {faculty.department}
        Research Domains: {domains}
        
        Suggest:
        1. Internal collaboration opportunities (different departments/schools)
        2. External collaboration opportunities (other institutions)
        3. Industry partnership possibilities
        4. Interdisciplinary research opportunities
        
        For each opportunity, provide:
        - Potential collaborator type/field
        - Research synergy explanation
        - Expected outcomes
        - Implementation strategy
        
        Format as structured JSON.
        """
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return [{"opportunities": response['message']['content']}]
            
        except Exception as e:
            print(f"Error identifying collaboration opportunities: {e}")
            return []
    
    def generate_career_development_plan(self, db: Session, faculty_id: int) -> Dict[str, Any]:
        faculty = crud.get_faculty(db, faculty_id)
        if not faculty:
            return {}
        
        overall_scores = crud.get_faculty_overall_scores(db, faculty_id)
        
        prompt = f"""
        Create a personalized career development plan for this faculty member:
        
        Faculty Profile:
        - Name: {faculty.first_name} {faculty.last_name}
        - Current Rank: {faculty.academic_rank}
        - Tenure Status: {faculty.tenure_status}
        - Years Experience: {faculty.years_experience}
        - Performance Scores: {json.dumps(overall_scores)}
        
        Provide:
        1. Short-term goals (1 year)
        2. Medium-term goals (2-3 years)
        3. Long-term career trajectory (5+ years)
        4. Specific milestones and metrics
        5. Resource requirements and support needs
        6. Potential obstacles and mitigation strategies
        
        Tailor recommendations to their current career stage and performance profile.
        """
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {"development_plan": response['message']['content']}
            
        except Exception as e:
            print(f"Error generating career development plan: {e}")
            return {"error": "Unable to generate development plan at this time."}

# Global AI service instance
faculty_ai_service = FacultyAIAnalysisService()