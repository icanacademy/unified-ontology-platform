
import sys
sys.path.append(".")
from database import SessionLocal
from models import Faculty, Research, Teaching
from datetime import datetime, timedelta
import json

db = SessionLocal()

# Sample faculty
sample_faculty = [
    {
        "faculty_id": "DR-001",
        "first_name": "Dr. Sarah",
        "last_name": "Johnson",
        "email": "sarah.johnson@university.edu",
        "department": "Computer Science",
        "academic_rank": "Associate Professor",
        "tenure_status": "Tenured",
        "hire_date": datetime(2018, 8, 15),
        "years_experience": 8,
        "properties": {"research_areas": ["AI", "Machine Learning"], "teaching_load": 2}
    },
    {
        "faculty_id": "DR-002", 
        "first_name": "Dr. Michael",
        "last_name": "Chen",
        "email": "michael.chen@university.edu",
        "department": "Mathematics",
        "academic_rank": "Full Professor",
        "tenure_status": "Tenured",
        "hire_date": datetime(2010, 9, 1),
        "years_experience": 15,
        "properties": {"research_areas": ["Statistics", "Data Science"], "teaching_load": 2}
    },
    {
        "faculty_id": "DR-003",
        "first_name": "Dr. Emily",
        "last_name": "Rodriguez",
        "email": "emily.rodriguez@university.edu", 
        "department": "Education",
        "academic_rank": "Assistant Professor",
        "tenure_status": "Tenure-track",
        "hire_date": datetime(2021, 1, 15),
        "years_experience": 3,
        "properties": {"research_areas": ["Educational Technology", "Learning Analytics"], "teaching_load": 3}
    }
]

for faculty_data in sample_faculty:
    existing = db.query(Faculty).filter(Faculty.faculty_id == faculty_data["faculty_id"]).first()
    if not existing:
        faculty = Faculty(**faculty_data)
        db.add(faculty)
        db.commit()
        
        # Add sample research for each faculty
        sample_research = Research(
            faculty_id=faculty.id,
            title=f"Research Paper by {faculty.first_name} {faculty.last_name}",
            publication_type="journal",
            venue="International Journal of Academic Excellence",
            publication_date=datetime.now() - timedelta(days=180),
            citation_count=25,
            impact_factor=2.5,
            co_author_count=3,
            primary_domain=faculty_data["properties"]["research_areas"][0]
        )
        db.add(sample_research)
        
        # Add sample teaching
        sample_teaching = Teaching(
            faculty_id=faculty.id,
            course_code="CS101",
            course_name="Introduction to Computing",
            semester="Fall",
            academic_year="2024",
            enrollment_count=45,
            completion_rate=0.92,
            average_grade=3.4,
            student_evaluation_score=4.2
        )
        db.add(sample_teaching)

db.commit()
db.close()
print("Sample data created successfully!")
