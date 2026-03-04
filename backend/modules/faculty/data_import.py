import csv
import io
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import crud, models, schemas
from fastapi import HTTPException

class FacultyDataImportService:
    def __init__(self):
        pass
    
    def parse_csv_data(self, data: str) -> List[List[str]]:
        """Parse CSV or tab-separated data from text input"""
        if '\t' in data and ',' not in data.split('\n')[0]:
            delimiter = '\t'
        else:
            delimiter = ','
        
        reader = csv.reader(io.StringIO(data.strip()), delimiter=delimiter)
        return list(reader)
    
    def import_faculty(self, db: Session, data: str) -> Dict[str, Any]:
        """Import faculty data from CSV format"""
        try:
            rows = self.parse_csv_data(data)
            imported_count = 0
            errors = []
            
            for i, row in enumerate(rows):
                try:
                    if len(row) < 8:
                        errors.append(f"Row {i+1}: Insufficient data (need 8 columns)")
                        continue
                    
                    faculty_id, first_name, last_name, email, department, academic_rank, tenure_status, years_exp = row[:8]
                    
                    existing = crud.get_faculty_by_faculty_id(db, faculty_id.strip())
                    if existing:
                        errors.append(f"Row {i+1}: Faculty {faculty_id} already exists")
                        continue
                    
                    faculty_create = schemas.FacultyCreate(
                        faculty_id=faculty_id.strip(),
                        first_name=first_name.strip(),
                        last_name=last_name.strip(),
                        email=email.strip(),
                        department=department.strip(),
                        academic_rank=academic_rank.strip(),
                        tenure_status=tenure_status.strip(),
                        hire_date=datetime.now(),
                        years_experience=int(years_exp.strip())
                    )
                    
                    crud.create_faculty(db, faculty_create)
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
            raise HTTPException(status_code=400, detail=f"Failed to parse faculty data: {str(e)}")
    
    def import_research(self, db: Session, data: str) -> Dict[str, Any]:
        """Import research data from CSV format"""
        try:
            rows = self.parse_csv_data(data)
            imported_count = 0
            errors = []
            
            for i, row in enumerate(rows):
                try:
                    if len(row) < 8:
                        errors.append(f"Row {i+1}: Insufficient data (need 8 columns)")
                        continue
                    
                    faculty_id, title, pub_type, venue, pub_date, citations, impact_factor, domain = row[:8]
                    
                    # Find faculty
                    faculty = crud.get_faculty_by_faculty_id(db, faculty_id.strip())
                    if not faculty:
                        errors.append(f"Row {i+1}: Faculty {faculty_id} not found")
                        continue
                    
                    # Parse date
                    try:
                        parsed_date = datetime.strptime(pub_date.strip(), "%Y-%m-%d")
                    except ValueError:
                        parsed_date = datetime.now()
                    
                    research_create = schemas.ResearchCreate(
                        faculty_id=faculty.id,
                        title=title.strip(),
                        publication_type=pub_type.strip(),
                        venue=venue.strip(),
                        publication_date=parsed_date,
                        citation_count=int(citations.strip()) if citations.strip() else 0,
                        impact_factor=float(impact_factor.strip()) if impact_factor.strip() else None,
                        co_author_count=1,
                        primary_domain=domain.strip()
                    )
                    
                    crud.create_research(db, research_create)
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
            raise HTTPException(status_code=400, detail=f"Failed to parse research data: {str(e)}")
    
    def import_teaching(self, db: Session, data: str) -> Dict[str, Any]:
        """Import teaching data from CSV format"""
        # Similar implementation for teaching data
        return {"imported_count": 0, "errors": ["Teaching import not yet implemented"], "total_rows": 0}
    

# Global import service instance
faculty_import_service = FacultyDataImportService()