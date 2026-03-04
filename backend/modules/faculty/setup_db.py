
import sys
import os
sys.path.append(os.getcwd())

try:
    from database import engine
    from models import Base, Faculty, Research, Teaching
    from datetime import datetime
    from database import SessionLocal
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Add sample data
    db = SessionLocal()
    
    # Check if data already exists
    existing_faculty = db.query(Faculty).first()
    if not existing_faculty:
        # Create sample faculty
        faculty1 = Faculty(
            faculty_id="DR-001",
            first_name="Dr. Sarah",
            last_name="Johnson", 
            email="sarah.johnson@university.edu",
            department="Computer Science",
            academic_rank="Associate Professor",
            tenure_status="Tenured",
            hire_date=datetime(2018, 8, 15),
            years_experience=8
        )
        
        faculty2 = Faculty(
            faculty_id="DR-002",
            first_name="Dr. Michael", 
            last_name="Chen",
            email="michael.chen@university.edu",
            department="Mathematics",
            academic_rank="Full Professor",
            tenure_status="Tenured",
            hire_date=datetime(2010, 9, 1),
            years_experience=15
        )
        
        db.add(faculty1)
        db.add(faculty2)
        db.commit()
        
        # Add sample research
        research1 = Research(
            faculty_id=faculty1.id,
            title="AI in Educational Technology",
            publication_type="journal",
            venue="Journal of Educational Computing Research",
            publication_date=datetime(2024, 3, 15),
            citation_count=42,
            impact_factor=2.8,
            co_author_count=3,
            primary_domain="Educational Technology"
        )
        
        db.add(research1)
        db.commit()
        
        print("Sample data created successfully!")
    else:
        print("Database already has data")
        
    db.close()
    
except Exception as e:
    print(f"Database setup error (continuing anyway): {e}")
