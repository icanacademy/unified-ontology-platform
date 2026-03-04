import csv
import io
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import crud, models, schemas
from fastapi import HTTPException

class DataImportService:
    def __init__(self):
        pass
    
    def parse_csv_data(self, data: str) -> List[List[str]]:
        """Parse CSV or tab-separated data from text input"""
        # Try to detect delimiter
        if '\t' in data and ',' not in data.split('\n')[0]:
            delimiter = '\t'
        else:
            delimiter = ','
        
        # Parse the data
        reader = csv.reader(io.StringIO(data.strip()), delimiter=delimiter)
        return list(reader)
    
    def import_students(self, db: Session, data: str) -> Dict[str, Any]:
        """Import student data from CSV format"""
        try:
            rows = self.parse_csv_data(data)
            imported_count = 0
            errors = []
            
            for i, row in enumerate(rows):
                try:
                    if len(row) < 5:
                        errors.append(f"Row {i+1}: Insufficient data (need 5 columns)")
                        continue
                    
                    student_id, first_name, last_name, email, grade_level = row[:5]
                    
                    # Check if student already exists
                    existing = crud.get_student_by_student_id(db, student_id.strip())
                    if existing:
                        errors.append(f"Row {i+1}: Student {student_id} already exists")
                        continue
                    
                    student_create = schemas.StudentCreate(
                        student_id=student_id.strip(),
                        first_name=first_name.strip(),
                        last_name=last_name.strip(),
                        email=email.strip(),
                        grade_level=int(grade_level.strip())
                    )
                    
                    crud.create_student(db, student_create)
                    imported_count += 1
                    
                except ValueError as e:
                    errors.append(f"Row {i+1}: Invalid data format - {str(e)}")
                except Exception as e:
                    errors.append(f"Row {i+1}: Error - {str(e)}")
            
            return {
                "imported_count": imported_count,
                "errors": errors,
                "total_rows": len(rows)
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse student data: {str(e)}")
    
    def import_teachers(self, db: Session, data: str) -> Dict[str, Any]:
        """Import teacher data from CSV format"""
        try:
            rows = self.parse_csv_data(data)
            imported_count = 0
            errors = []
            
            for i, row in enumerate(rows):
                try:
                    if len(row) < 6:
                        errors.append(f"Row {i+1}: Insufficient data (need 6 columns)")
                        continue
                    
                    teacher_id, first_name, last_name, email, department, years_experience = row[:6]
                    
                    # Check if teacher already exists
                    existing = db.query(models.Teacher).filter(
                        models.Teacher.teacher_id == teacher_id.strip()
                    ).first()
                    if existing:
                        errors.append(f"Row {i+1}: Teacher {teacher_id} already exists")
                        continue
                    
                    teacher_create = schemas.TeacherCreate(
                        teacher_id=teacher_id.strip(),
                        first_name=first_name.strip(),
                        last_name=last_name.strip(),
                        email=email.strip(),
                        department=department.strip(),
                        years_experience=int(years_experience.strip())
                    )
                    
                    crud.create_teacher(db, teacher_create)
                    imported_count += 1
                    
                except ValueError as e:
                    errors.append(f"Row {i+1}: Invalid data format - {str(e)}")
                except Exception as e:
                    errors.append(f"Row {i+1}: Error - {str(e)}")
            
            return {
                "imported_count": imported_count,
                "errors": errors,
                "total_rows": len(rows)
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse teacher data: {str(e)}")
    
    def import_courses(self, db: Session, data: str) -> Dict[str, Any]:
        """Import course data from CSV format"""
        try:
            rows = self.parse_csv_data(data)
            imported_count = 0
            errors = []
            
            for i, row in enumerate(rows):
                try:
                    if len(row) < 6:
                        errors.append(f"Row {i+1}: Insufficient data (need 6 columns)")
                        continue
                    
                    course_code, course_name, subject, difficulty_level, credits, teacher_id = row[:6]
                    
                    # Check if course already exists
                    existing = db.query(models.Course).filter(
                        models.Course.course_code == course_code.strip()
                    ).first()
                    if existing:
                        errors.append(f"Row {i+1}: Course {course_code} already exists")
                        continue
                    
                    # Find teacher
                    teacher = db.query(models.Teacher).filter(
                        models.Teacher.teacher_id == teacher_id.strip()
                    ).first()
                    if not teacher:
                        errors.append(f"Row {i+1}: Teacher {teacher_id} not found")
                        continue
                    
                    course_create = schemas.CourseCreate(
                        course_code=course_code.strip(),
                        course_name=course_name.strip(),
                        subject=subject.strip(),
                        difficulty_level=int(difficulty_level.strip()),
                        credits=int(credits.strip()),
                        teacher_id=teacher.id
                    )
                    
                    crud.create_course(db, course_create)
                    imported_count += 1
                    
                except ValueError as e:
                    errors.append(f"Row {i+1}: Invalid data format - {str(e)}")
                except Exception as e:
                    errors.append(f"Row {i+1}: Error - {str(e)}")
            
            return {
                "imported_count": imported_count,
                "errors": errors,
                "total_rows": len(rows)
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse course data: {str(e)}")
    
    def import_assessments(self, db: Session, data: str) -> Dict[str, Any]:
        """Import assessment data from CSV format"""
        try:
            rows = self.parse_csv_data(data)
            imported_count = 0
            errors = []
            
            for i, row in enumerate(rows):
                try:
                    if len(row) < 7:
                        errors.append(f"Row {i+1}: Insufficient data (need 7 columns)")
                        continue
                    
                    student_id, course_code, assessment_type, title, score, max_score, assessment_date = row[:7]
                    
                    # Find student
                    student = crud.get_student_by_student_id(db, student_id.strip())
                    if not student:
                        errors.append(f"Row {i+1}: Student {student_id} not found")
                        continue
                    
                    # Find course
                    course = db.query(models.Course).filter(
                        models.Course.course_code == course_code.strip()
                    ).first()
                    if not course:
                        errors.append(f"Row {i+1}: Course {course_code} not found")
                        continue
                    
                    # Parse date
                    try:
                        parsed_date = datetime.strptime(assessment_date.strip(), "%Y-%m-%d")
                    except ValueError:
                        try:
                            parsed_date = datetime.strptime(assessment_date.strip(), "%m/%d/%Y")
                        except ValueError:
                            errors.append(f"Row {i+1}: Invalid date format (use YYYY-MM-DD or MM/DD/YYYY)")
                            continue
                    
                    assessment_create = schemas.AssessmentCreate(
                        student_id=student.id,
                        course_id=course.id,
                        assessment_type=assessment_type.strip(),
                        title=title.strip(),
                        score=float(score.strip()),
                        max_score=float(max_score.strip()),
                        assessment_date=parsed_date,
                        submitted_date=parsed_date
                    )
                    
                    crud.create_assessment(db, assessment_create)
                    imported_count += 1
                    
                except ValueError as e:
                    errors.append(f"Row {i+1}: Invalid data format - {str(e)}")
                except Exception as e:
                    errors.append(f"Row {i+1}: Error - {str(e)}")
            
            return {
                "imported_count": imported_count,
                "errors": errors,
                "total_rows": len(rows)
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse assessment data: {str(e)}")
    
    def import_attendance(self, db: Session, data: str) -> Dict[str, Any]:
        """Import attendance data from CSV format"""
        try:
            rows = self.parse_csv_data(data)
            imported_count = 0
            errors = []
            
            for i, row in enumerate(rows):
                try:
                    if len(row) < 4:
                        errors.append(f"Row {i+1}: Insufficient data (need 4 columns)")
                        continue
                    
                    student_id, course_code, date, status = row[:4]
                    
                    # Find student
                    student = crud.get_student_by_student_id(db, student_id.strip())
                    if not student:
                        errors.append(f"Row {i+1}: Student {student_id} not found")
                        continue
                    
                    # Find course
                    course = db.query(models.Course).filter(
                        models.Course.course_code == course_code.strip()
                    ).first()
                    if not course:
                        errors.append(f"Row {i+1}: Course {course_code} not found")
                        continue
                    
                    # Parse date
                    try:
                        parsed_date = datetime.strptime(date.strip(), "%Y-%m-%d")
                    except ValueError:
                        try:
                            parsed_date = datetime.strptime(date.strip(), "%m/%d/%Y")
                        except ValueError:
                            errors.append(f"Row {i+1}: Invalid date format (use YYYY-MM-DD or MM/DD/YYYY)")
                            continue
                    
                    # Validate status
                    valid_statuses = ['present', 'absent', 'late', 'excused']
                    if status.strip().lower() not in valid_statuses:
                        errors.append(f"Row {i+1}: Invalid status '{status}'. Must be one of: {valid_statuses}")
                        continue
                    
                    attendance_create = schemas.AttendanceCreate(
                        student_id=student.id,
                        course_id=course.id,
                        date=parsed_date,
                        status=status.strip().lower()
                    )
                    
                    crud.create_attendance(db, attendance_create)
                    imported_count += 1
                    
                except ValueError as e:
                    errors.append(f"Row {i+1}: Invalid data format - {str(e)}")
                except Exception as e:
                    errors.append(f"Row {i+1}: Error - {str(e)}")
            
            return {
                "imported_count": imported_count,
                "errors": errors,
                "total_rows": len(rows)
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse attendance data: {str(e)}")

# Global import service instance
import_service = DataImportService()