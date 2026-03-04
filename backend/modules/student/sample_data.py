from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from database import SessionLocal
import crud
import schemas

def create_sample_data():
    db = SessionLocal()
    
    try:
        # Create sample teachers
        teachers_data = [
            {"teacher_id": "T001", "first_name": "Sarah", "last_name": "Johnson", "email": "s.johnson@school.edu", "department": "Mathematics", "years_experience": 8},
            {"teacher_id": "T002", "first_name": "Michael", "last_name": "Chen", "email": "m.chen@school.edu", "department": "Science", "years_experience": 12},
            {"teacher_id": "T003", "first_name": "Emily", "last_name": "Rodriguez", "email": "e.rodriguez@school.edu", "department": "English", "years_experience": 6},
            {"teacher_id": "T004", "first_name": "David", "last_name": "Williams", "email": "d.williams@school.edu", "department": "History", "years_experience": 15},
        ]
        
        teachers = []
        for teacher_data in teachers_data:
            teacher = crud.create_teacher(db, schemas.TeacherCreate(**teacher_data))
            teachers.append(teacher)
            print(f"Created teacher: {teacher.first_name} {teacher.last_name}")
        
        # Create sample courses
        courses_data = [
            {"course_code": "MATH101", "course_name": "Algebra I", "subject": "Mathematics", "difficulty_level": 2, "credits": 3, "teacher_id": teachers[0].id},
            {"course_code": "SCI201", "course_name": "Biology", "subject": "Science", "difficulty_level": 3, "credits": 4, "teacher_id": teachers[1].id},
            {"course_code": "ENG101", "course_name": "English Literature", "subject": "English", "difficulty_level": 2, "credits": 3, "teacher_id": teachers[2].id},
            {"course_code": "HIST301", "course_name": "World History", "subject": "History", "difficulty_level": 4, "credits": 3, "teacher_id": teachers[3].id},
            {"course_code": "MATH201", "course_name": "Geometry", "subject": "Mathematics", "difficulty_level": 3, "credits": 3, "teacher_id": teachers[0].id},
        ]
        
        courses = []
        for course_data in courses_data:
            course = crud.create_course(db, schemas.CourseCreate(**course_data))
            courses.append(course)
            print(f"Created course: {course.course_name}")
        
        # Create sample students
        students_data = [
            {"student_id": "S001", "first_name": "Alice", "last_name": "Smith", "email": "alice.smith@student.edu", "grade_level": 9},
            {"student_id": "S002", "first_name": "Bob", "last_name": "Jones", "email": "bob.jones@student.edu", "grade_level": 10},
            {"student_id": "S003", "first_name": "Carol", "last_name": "Brown", "email": "carol.brown@student.edu", "grade_level": 11},
            {"student_id": "S004", "first_name": "David", "last_name": "Wilson", "email": "david.wilson@student.edu", "grade_level": 9},
            {"student_id": "S005", "first_name": "Eva", "last_name": "Davis", "email": "eva.davis@student.edu", "grade_level": 12},
            {"student_id": "S006", "first_name": "Frank", "last_name": "Miller", "email": "frank.miller@student.edu", "grade_level": 10},
            {"student_id": "S007", "first_name": "Grace", "last_name": "Garcia", "email": "grace.garcia@student.edu", "grade_level": 11},
            {"student_id": "S008", "first_name": "Henry", "last_name": "Martinez", "email": "henry.martinez@student.edu", "grade_level": 9},
        ]
        
        students = []
        for student_data in students_data:
            student = crud.create_student(db, schemas.StudentCreate(**student_data))
            students.append(student)
            print(f"Created student: {student.first_name} {student.last_name}")
        
        # Create sample assessments
        assessment_types = ["quiz", "exam", "assignment", "project"]
        
        for student in students:
            for course in courses:
                # Create 3-5 assessments per student per course
                num_assessments = random.randint(3, 5)
                for i in range(num_assessments):
                    # Generate realistic scores based on student "ability"
                    base_score = random.uniform(0.6, 0.95)  # Students generally do okay to well
                    if student.student_id in ["S001", "S003", "S005"]:  # Some students perform better
                        base_score = random.uniform(0.8, 0.98)
                    elif student.student_id in ["S004", "S008"]:  # Some struggle more
                        base_score = random.uniform(0.5, 0.8)
                    
                    max_score = 100
                    score = base_score * max_score
                    
                    assessment_date = datetime.now() - timedelta(days=random.randint(1, 120))
                    
                    assessment = schemas.AssessmentCreate(
                        student_id=student.id,
                        course_id=course.id,
                        assessment_type=random.choice(assessment_types),
                        title=f"{course.subject} {random.choice(['Quiz', 'Test', 'Assignment', 'Project'])} #{i+1}",
                        score=round(score, 1),
                        max_score=max_score,
                        assessment_date=assessment_date,
                        submitted_date=assessment_date + timedelta(hours=random.randint(1, 24))
                    )
                    
                    crud.create_assessment(db, assessment)
        
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()