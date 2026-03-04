import ollama
import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import crud
import schemas
import os

class AIAnalysisService:
    def __init__(self, model_name: str = "llama3.1"):
        self.model_name = model_name
        self.client = ollama.Client(host=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    
    def analyze_student_performance(self, db: Session, student_id: int) -> List[schemas.InsightCreate]:
        student = crud.get_student(db, student_id)
        if not student:
            return []
        
        assessments = crud.get_student_assessments(db, student_id)
        gpa = crud.get_student_gpa(db, student_id)
        subject_performance = crud.get_student_subject_performance(db, student_id)
        attendance_rate = crud.get_student_attendance_rate(db, student_id)
        
        student_data = {
            "student_info": {
                "name": f"{student.first_name} {student.last_name}",
                "grade_level": student.grade_level,
                "overall_gpa": gpa,
                "attendance_rate": attendance_rate
            },
            "subject_performance": subject_performance,
            "recent_assessments": [
                {
                    "type": a.assessment_type,
                    "score_percentage": (a.score / a.max_score) * 100,
                    "subject": db.query(crud.models.Course).filter(crud.models.Course.id == a.course_id).first().subject
                }
                for a in assessments[-10:]  # Last 10 assessments
            ]
        }
        
        prompt = f"""
        Analyze this student's academic performance data and provide insights:
        
        Student Data: {json.dumps(student_data, indent=2)}
        
        Please provide:
        1. 2-3 key academic strengths with confidence scores (0.0-1.0)
        2. 2-3 key academic weaknesses with confidence scores (0.0-1.0)  
        3. 3-4 specific, actionable recommendations for teachers
        
        Format your response as JSON with this structure:
        {{
            "strengths": [
                {{"description": "strength description", "category": "academic", "confidence": 0.85}}
            ],
            "weaknesses": [
                {{"description": "weakness description", "category": "academic", "confidence": 0.75}}
            ],
            "recommendations": [
                {{"description": "specific teaching recommendation", "category": "academic", "confidence": 0.90}}
            ]
        }}
        
        Be specific and actionable in your recommendations.
        """
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            
            analysis = json.loads(response['message']['content'])
            insights = []
            
            # Create insight objects for strengths
            for strength in analysis.get('strengths', []):
                insights.append(schemas.InsightCreate(
                    student_id=student_id,
                    insight_type="strength",
                    category=strength.get('category', 'academic'),
                    description=strength['description'],
                    confidence_score=strength.get('confidence', 0.8),
                    model_used=self.model_name,
                    data_sources=["assessments", "gpa", "attendance", "subject_performance"]
                ))
            
            # Create insight objects for weaknesses
            for weakness in analysis.get('weaknesses', []):
                insights.append(schemas.InsightCreate(
                    student_id=student_id,
                    insight_type="weakness",
                    category=weakness.get('category', 'academic'),
                    description=weakness['description'],
                    confidence_score=weakness.get('confidence', 0.8),
                    model_used=self.model_name,
                    data_sources=["assessments", "gpa", "attendance", "subject_performance"]
                ))
            
            # Create insight objects for recommendations
            for recommendation in analysis.get('recommendations', []):
                insights.append(schemas.InsightCreate(
                    student_id=student_id,
                    insight_type="recommendation",
                    category=recommendation.get('category', 'academic'),
                    description=recommendation['description'],
                    confidence_score=recommendation.get('confidence', 0.8),
                    model_used=self.model_name,
                    data_sources=["assessments", "gpa", "attendance", "subject_performance"]
                ))
            
            return insights
            
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            return []
    
    def generate_teaching_strategies(self, db: Session, student_id: int, weakness_area: str) -> str:
        student = crud.get_student(db, student_id)
        if not student:
            return ""
        
        prompt = f"""
        Generate specific teaching strategies to help a grade {student.grade_level} student improve in {weakness_area}.
        
        Provide 3-4 concrete, actionable strategies that a teacher can implement immediately.
        Focus on practical classroom techniques, learning accommodations, and engagement methods.
        
        Format as a numbered list.
        """
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response['message']['content']
            
        except Exception as e:
            print(f"Error generating teaching strategies: {e}")
            return "Unable to generate teaching strategies at this time."

# Global AI service instance
ai_service = AIAnalysisService()