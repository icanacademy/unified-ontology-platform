import re
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from assessment_models import LevelTest, InterviewAssessment, SkillProgression, StudentProgress

class AssessmentImportService:
    def __init__(self):
        pass
    
    def parse_level_test_data(self, data: str) -> Dict[str, Any]:
        """Parse level test data from the formatted text input"""
        try:
            # Clean up the data - normalize whitespace while preserving structure
            cleaned_data = re.sub(r'\s+', ' ', data)  # Replace multiple spaces with single space
            cleaned_data = re.sub(r'\s*\n\s*', '\n', cleaned_data)  # Clean line breaks
            
            # Extract basic information with more flexible patterns
            name_match = re.search(r'Name:\s*([^\n\r]+?)(?:\s+Date:)', data, re.IGNORECASE)
            date_match = re.search(r'Date:\s*(\d{1,2}/\d{1,2}/\d{4})', data)
            grade_match = re.search(r'Grade:\s*([^\n\r]+?)(?:\s+Test type:)', data, re.IGNORECASE)
            test_type_match = re.search(r'Test type:\s*([^\n\r]+?)(?:\s|$)', data, re.IGNORECASE)
            
            # Extract scores with more flexible patterns
            grammar_match = re.search(r'Grammar\s+(\d+)/(\d+)', data, re.IGNORECASE)
            reading_match = re.search(r'Reading\s+(\d+)/(\d+)', data, re.IGNORECASE)
            vocabulary_match = re.search(r'Vocabulary\s+(\d+)/(\d+)', data, re.IGNORECASE)
            listening_match = re.search(r'Listening\s+(\d+)/(\d+)', data, re.IGNORECASE)
            writing_match = re.search(r'Writing\s+(?:(\d+))?/(\d+)', data, re.IGNORECASE)
            total_match = re.search(r'Total\s+(\d+)/(\d+)', data, re.IGNORECASE)
            
            # Extract recommendation - simpler pattern
            recommendation_match = re.search(r'Recommendation:\s*(.*?)(?=Student|📝|✅|❌|$)', data, re.DOTALL | re.IGNORECASE)
            
            # Extract written response - look for text between quotes after "Student's Written Response:"
            written_response_match = re.search(r'Student[\'s] Written Response:\s*["\"]([^"\"]*)["\"]', data, re.DOTALL)
            if not written_response_match:
                written_response_match = re.search(r'Student[\'s] Written Response:\s*["""]([^"""]*)["""]', data, re.DOTALL)
            
            # Extract writing analysis - look for text between quotes after the writing emoji
            writing_analysis_match = re.search(r'📝\s*Assessment of Writing\s*["\"]([^"\"]*)["\"]', data, re.DOTALL)
            
            # Extract strengths and weaknesses - look for text between quotes after emojis
            strengths_match = re.search(r'✅\s*Strengths\s*["\"]([^"\"]*)["\"]', data, re.DOTALL)
            weaknesses_match = re.search(r'❌\s*Weaknesses\s*["\"]([^"\"]*)["\"]', data, re.DOTALL)
            
            # Parse date
            test_date = None
            if date_match:
                try:
                    test_date = datetime.strptime(date_match.group(1), "%m/%d/%Y")
                except ValueError:
                    pass
            
            # Parse writing score (might be empty)
            writing_score = None
            writing_total = 20  # default
            if writing_match:
                if writing_match.group(1):
                    writing_score = int(writing_match.group(1))
                writing_total = int(writing_match.group(2))
            
            # Clean and format extracted text
            def clean_text(text):
                if not text:
                    return ""
                # Remove excessive whitespace but preserve paragraphs
                text = re.sub(r'\s+', ' ', text.strip())
                text = re.sub(r'\s*\n\s*', '\n', text)
                return text.strip()

            return {
                "student_name": clean_text(name_match.group(1)) if name_match else "",
                "test_date": test_date,
                "grade": clean_text(grade_match.group(1)) if grade_match else "",
                "test_level": clean_text(test_type_match.group(1)) if test_type_match else "",
                "grammar_score": int(grammar_match.group(1)) if grammar_match else 0,
                "grammar_total": int(grammar_match.group(2)) if grammar_match else 30,
                "reading_score": int(reading_match.group(1)) if reading_match else 0,
                "reading_total": int(reading_match.group(2)) if reading_match else 30,
                "vocabulary_score": int(vocabulary_match.group(1)) if vocabulary_match else 0,
                "vocabulary_total": int(vocabulary_match.group(2)) if vocabulary_match else 20,
                "listening_score": int(listening_match.group(1)) if listening_match else 0,
                "listening_total": int(listening_match.group(2)) if listening_match else 20,
                "writing_score": writing_score,
                "writing_total": writing_total,
                "total_score": int(total_match.group(1)) if total_match else 0,
                "total_possible": int(total_match.group(2)) if total_match else 120,
                "ai_recommendation": clean_text(recommendation_match.group(1)) if recommendation_match else "",
                "writing_response": clean_text(written_response_match.group(1)) if written_response_match else "",
                "writing_analysis": clean_text(writing_analysis_match.group(1)) if writing_analysis_match else "",
                "strengths": clean_text(strengths_match.group(1)) if strengths_match else "",
                "weaknesses": clean_text(weaknesses_match.group(1)) if weaknesses_match else ""
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse level test data: {str(e)}")
    
    def parse_interview_data(self, data: str) -> Dict[str, Any]:
        """Parse interview assessment data from the formatted text input"""
        try:
            # Clean and format extracted text
            def clean_text(text):
                if not text:
                    return ""
                # Remove excessive whitespace but preserve paragraphs
                text = re.sub(r'\s+', ' ', text.strip())
                text = re.sub(r'\s*\n\s*', '\n', text)
                return text.strip()
            
            # Extract basic information with flexible whitespace handling
            name_match = re.search(r'NAME:\s*([^\n\r]+)', data, re.IGNORECASE)
            id_match = re.search(r'ID NUMBER:\s*([^\n\r]+)', data, re.IGNORECASE)
            age_match = re.search(r'AGE:\s*(\d+)', data, re.IGNORECASE)
            level_match = re.search(r'LEVEL:\s*([^\n\r]+)', data, re.IGNORECASE)
            date_match = re.search(r'DATE:\s*([^\n\r]+)', data, re.IGNORECASE)
            interviewer_match = re.search(r'INTERVIEWER:\s*([^\n\r]+)', data, re.IGNORECASE)
            
            # Extract initial and final scores
            initial_score_match = re.search(r'INITIAL INTERVIEW SCORE\s*(\d+(?:\.\d+)?)/(\d+)', data, re.IGNORECASE)
            final_score_match = re.search(r'FINAL INTERVIEW SCORE\s*(\d+(?:\.\d+)?|TBD)', data, re.IGNORECASE)
            
            # Extract detailed criteria scores - look for patterns with flexible spacing
            pronunciation_match = re.search(r'(?:10%\s*)?Pronunciation[/\s]*Accent\s+([\d.]+)', data, re.IGNORECASE)
            fluency_match = re.search(r'(?:60%\s*)?Fluency\s+([\d.]+)', data, re.IGNORECASE)
            comprehension_match = re.search(r'(?:10%\s*)?Comprehension\s+([\d.]+)', data, re.IGNORECASE)
            insight_match = re.search(r'(?:10%\s*)?Insight\s+([\d.]+)', data, re.IGNORECASE)
            vocab_mechanics_match = re.search(r'(?:10%\s*)?Vocab[/\s]*Mechanics\s+([\d.]+)', data, re.IGNORECASE)
            
            # Extract rhetoric scores with flexible patterns
            clarity_match = re.search(r'(?:25%\s*)?Clarity\s+([\d.]+)', data, re.IGNORECASE)
            evidence_match = re.search(r'(?:20%\s*)?Evidence\s+([\d.]+)', data, re.IGNORECASE)
            articulation_match = re.search(r'(?:20%\s*)?Articulation\s+([\d.]+)', data, re.IGNORECASE)
            techniques_match = re.search(r'(?:15%\s*)?Techniques\s+([\d.]+)', data, re.IGNORECASE)
            impact_match = re.search(r'(?:20%\s*)?Impact\s+([\d.]+)', data, re.IGNORECASE)
            
            # Extract knowledge level
            knowledge_level_match = re.search(r'KL\s*(\d)', data, re.IGNORECASE)
            
            # Extract question scores (N6, D7, E8, A2, P9) - look for scores in table
            question_scores = {}
            for q in ['N6', 'D7', 'E8', 'A2', 'P9']:
                # Try different patterns for question scores
                q_match = re.search(rf'{q}\s+(\d+)', data) or re.search(rf'{q}\s*1', data)
                if q_match:
                    try:
                        question_scores[q] = int(q_match.group(1))
                    except:
                        question_scores[q] = 1  # Default if pattern matched but extraction failed
            
            # Extract analysis with flexible quotes
            analysis_match = re.search(r'ANALYSIS\s*["\"]([^"\"]*)["\"]', data, re.DOTALL | re.IGNORECASE)
            
            # Parse date
            test_date = None
            if date_match:
                try:
                    date_str = date_match.group(1).strip()
                    test_date = datetime.strptime(date_str, "%A, %B %d, %Y")
                except ValueError:
                    try:
                        test_date = datetime.strptime(date_str, "%m/%d/%Y")
                    except ValueError:
                        pass
            
            # Parse final score
            final_score = None
            if final_score_match and final_score_match.group(1) != 'TBD':
                final_score = float(final_score_match.group(1))
            
            return {
                "student_name": clean_text(name_match.group(1)) if name_match else "",
                "student_id": clean_text(id_match.group(1)) if id_match else "",
                "age": int(age_match.group(1)) if age_match else 0,
                "level": clean_text(level_match.group(1)) if level_match else "",
                "test_date": test_date,
                "interviewer": clean_text(interviewer_match.group(1)) if interviewer_match else "",
                "initial_score": float(initial_score_match.group(1)) if initial_score_match else 0.0,
                "final_score": final_score,
                "total_possible": float(initial_score_match.group(2)) if initial_score_match else 20.0,
                "pronunciation_score": float(pronunciation_match.group(1)) if pronunciation_match else 0.0,
                "fluency_score": float(fluency_match.group(1)) if fluency_match else 0.0,
                "comprehension_score": float(comprehension_match.group(1)) if comprehension_match else 0.0,
                "insight_score": float(insight_match.group(1)) if insight_match else 0.0,
                "vocabulary_score": float(vocab_mechanics_match.group(1)) if vocab_mechanics_match else 0.0,
                "rhetoric_clarity": float(clarity_match.group(1)) if clarity_match else 0.0,
                "rhetoric_evidence": float(evidence_match.group(1)) if evidence_match else 0.0,
                "rhetoric_articulation": float(articulation_match.group(1)) if articulation_match else 0.0,
                "rhetoric_techniques": float(techniques_match.group(1)) if techniques_match else 0.0,
                "rhetoric_impact": float(impact_match.group(1)) if impact_match else 0.0,
                "knowledge_level": int(knowledge_level_match.group(1)) if knowledge_level_match else 1,
                "question_scores": question_scores,
                "analysis_text": clean_text(analysis_match.group(1)) if analysis_match else ""
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse interview data: {str(e)}")
    
    def import_level_test(self, db: Session, data: str) -> Dict[str, Any]:
        """Import a level test assessment"""
        try:
            parsed_data = self.parse_level_test_data(data)
            
            # Create level test record
            level_test = LevelTest(
                student_name=parsed_data["student_name"],
                student_id=f"LT-{parsed_data['student_name'].replace(' ', '-')}-{datetime.now().strftime('%Y%m%d')}",
                grade=parsed_data["grade"],
                test_level=parsed_data["test_level"],
                test_date=parsed_data["test_date"] or datetime.now(),
                grammar_score=parsed_data["grammar_score"],
                grammar_total=parsed_data["grammar_total"],
                reading_score=parsed_data["reading_score"],
                reading_total=parsed_data["reading_total"],
                vocabulary_score=parsed_data["vocabulary_score"],
                vocabulary_total=parsed_data["vocabulary_total"],
                listening_score=parsed_data["listening_score"],
                listening_total=parsed_data["listening_total"],
                writing_score=parsed_data["writing_score"],
                writing_total=parsed_data["writing_total"],
                total_score=parsed_data["total_score"],
                total_possible=parsed_data["total_possible"],
                ai_recommendation=parsed_data["ai_recommendation"],
                writing_response=parsed_data["writing_response"],
                writing_analysis=parsed_data["writing_analysis"],
                strengths={"analysis": parsed_data["strengths"]},
                weaknesses={"analysis": parsed_data["weaknesses"]}
            )
            
            db.add(level_test)
            db.commit()
            db.refresh(level_test)
            
            # Create skill progression records
            self.create_skill_progressions(db, level_test)
            
            # Update student progress
            self.update_student_progress(db, level_test.student_id, level_test.student_name, level_test.id, None)
            
            return {
                "imported_count": 1,
                "assessment_id": level_test.id,
                "student_name": level_test.student_name,
                "total_score": f"{level_test.total_score}/{level_test.total_possible}",
                "errors": []
            }
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Failed to import level test: {str(e)}")
    
    def import_interview_assessment(self, db: Session, data: str) -> Dict[str, Any]:
        """Import an interview assessment"""
        try:
            parsed_data = self.parse_interview_data(data)
            
            # Calculate rhetoric total
            rhetoric_total = sum([
                parsed_data["rhetoric_clarity"],
                parsed_data["rhetoric_evidence"], 
                parsed_data["rhetoric_articulation"],
                parsed_data["rhetoric_techniques"],
                parsed_data["rhetoric_impact"]
            ])
            
            # Create interview assessment record
            interview = InterviewAssessment(
                student_name=parsed_data["student_name"],
                student_id=parsed_data["student_id"],
                age=parsed_data["age"],
                level=parsed_data["level"],
                test_date=parsed_data["test_date"] or datetime.now(),
                interviewer=parsed_data["interviewer"],
                initial_score=parsed_data["initial_score"],
                final_score=parsed_data["final_score"],
                total_possible=parsed_data["total_possible"],
                pronunciation_score=parsed_data["pronunciation_score"],
                fluency_score=parsed_data["fluency_score"],
                comprehension_score=parsed_data["comprehension_score"],
                insight_score=parsed_data["insight_score"],
                vocabulary_score=parsed_data["vocabulary_score"],
                rhetoric_clarity=parsed_data["rhetoric_clarity"],
                rhetoric_evidence=parsed_data["rhetoric_evidence"],
                rhetoric_articulation=parsed_data["rhetoric_articulation"],
                rhetoric_techniques=parsed_data["rhetoric_techniques"],
                rhetoric_impact=parsed_data["rhetoric_impact"],
                rhetoric_total=rhetoric_total,
                knowledge_level=parsed_data["knowledge_level"],
                question_scores=parsed_data["question_scores"],
                analysis_text=parsed_data["analysis_text"]
            )
            
            db.add(interview)
            db.commit()
            db.refresh(interview)
            
            # Create skill progression records for speaking skills
            self.create_interview_skill_progressions(db, interview)
            
            # Update student progress
            self.update_student_progress(db, interview.student_id, interview.student_name, None, interview.id)
            
            return {
                "imported_count": 1,
                "assessment_id": interview.id,
                "student_name": interview.student_name,
                "initial_score": f"{interview.initial_score}/{interview.total_possible}",
                "errors": []
            }
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Failed to import interview assessment: {str(e)}")
    
    def create_skill_progressions(self, db: Session, level_test: LevelTest):
        """Create skill progression records for level test"""
        skills = [
            ("grammar", level_test.grammar_score, level_test.grammar_total),
            ("reading", level_test.reading_score, level_test.reading_total),
            ("vocabulary", level_test.vocabulary_score, level_test.vocabulary_total),
            ("listening", level_test.listening_score, level_test.listening_total)
        ]
        
        if level_test.writing_score is not None:
            skills.append(("writing", level_test.writing_score, level_test.writing_total))
        
        for skill_name, score, max_score in skills:
            if score is not None and max_score > 0:
                progression = SkillProgression(
                    student_id=level_test.student_id,
                    skill_name=skill_name,
                    score=float(score),
                    max_score=float(max_score),
                    percentage=(score / max_score) * 100,
                    assessment_type="level_test",
                    assessment_id=level_test.id,
                    test_date=level_test.test_date
                )
                db.add(progression)
        
        db.commit()
    
    def create_interview_skill_progressions(self, db: Session, interview: InterviewAssessment):
        """Create skill progression records for interview"""
        skills = [
            ("pronunciation", interview.pronunciation_score, 2.0),
            ("fluency", interview.fluency_score, 2.0),
            ("comprehension", interview.comprehension_score, 2.0),
            ("insight", interview.insight_score, 2.0),
            ("vocabulary", interview.vocabulary_score, 2.0),
            ("speaking_overall", interview.initial_score, interview.total_possible)
        ]
        
        for skill_name, score, max_score in skills:
            if score is not None and max_score > 0:
                progression = SkillProgression(
                    student_id=interview.student_id,
                    skill_name=skill_name,
                    score=float(score),
                    max_score=float(max_score),
                    percentage=(score / max_score) * 100,
                    assessment_type="interview",
                    assessment_id=interview.id,
                    test_date=interview.test_date
                )
                db.add(progression)
        
        db.commit()
    
    def update_student_progress(self, db: Session, student_id: str, student_name: str, 
                               level_test_id: Optional[int] = None, interview_id: Optional[int] = None):
        """Update or create student progress record"""
        progress = db.query(StudentProgress).filter(StudentProgress.student_id == student_id).first()
        
        if not progress:
            progress = StudentProgress(
                student_id=student_id,
                student_name=student_name,
                total_assessments=0
            )
            db.add(progress)
        
        # Update latest assessment info
        if level_test_id:
            progress.latest_level_test_id = level_test_id
        if interview_id:
            progress.latest_interview_id = interview_id
        
        progress.latest_test_date = datetime.now()
        progress.total_assessments += 1
        progress.updated_at = datetime.now()
        
        # Update current skill levels from latest progressions
        latest_skills = db.query(SkillProgression).filter(
            SkillProgression.student_id == student_id
        ).order_by(SkillProgression.test_date.desc()).limit(10).all()
        
        skill_map = {}
        for skill in latest_skills:
            if skill.skill_name not in skill_map:
                skill_map[skill.skill_name] = skill.percentage
        
        # Update current skill levels
        progress.current_grammar = skill_map.get("grammar")
        progress.current_reading = skill_map.get("reading")
        progress.current_vocabulary = skill_map.get("vocabulary")
        progress.current_listening = skill_map.get("listening")
        progress.current_writing = skill_map.get("writing")
        progress.current_speaking = skill_map.get("speaking_overall")
        
        db.commit()

# Global assessment import service instance
assessment_import_service = AssessmentImportService()