from fastapi import FastAPI, Depends, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta
import crud, models, schemas
from database import SessionLocal, engine
from pydantic import BaseModel

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Books & Library Management Platform",
    description="Comprehensive library management system with AI-powered features",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3004", "http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# ROOT AND HEALTH ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    return {
        "message": "Books & Library Management Platform API",
        "version": "1.0.0",
        "description": "AI-Powered Comprehensive Library System"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# ============================================================================
# BOOK MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Create a new book"""
    # Check if book with same ISBN already exists
    if book.isbn_10 and crud.get_book_by_isbn(db, book.isbn_10):
        raise HTTPException(status_code=400, detail="Book with this ISBN-10 already exists")
    if book.isbn_13 and crud.get_book_by_isbn(db, book.isbn_13):
        raise HTTPException(status_code=400, detail="Book with this ISBN-13 already exists")
    
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=List[schemas.Book])
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get list of all books with pagination"""
    return crud.get_books(db, skip=skip, limit=limit)

@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """Get book by ID"""
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int = Path(..., ge=1),
    book_update: schemas.BookUpdate = None,
    db: Session = Depends(get_db)
):
    """Update book information"""
    book = crud.update_book(db, book_id=book_id, book_update=book_update)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """Delete a book"""
    if not crud.delete_book(db, book_id=book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

@app.post("/books/search", response_model=List[schemas.Book])
def search_books(search_params: schemas.BookSearch, db: Session = Depends(get_db)):
    """Advanced book search"""
    return crud.search_books(db, search_params)

@app.get("/books/popular/trending", response_model=List[schemas.Book])
def get_popular_books(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    """Get most popular books"""
    return crud.get_popular_books(db, limit=limit)

@app.get("/books/recent/additions", response_model=List[schemas.Book])
def get_recent_books(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    """Get recently added books"""
    return crud.get_recently_added_books(db, limit=limit)

@app.get("/books/isbn/{isbn}", response_model=schemas.Book)
def get_book_by_isbn(isbn: str = Path(..., min_length=10, max_length=17), db: Session = Depends(get_db)):
    """Get book by ISBN"""
    book = crud.get_book_by_isbn(db, isbn=isbn)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# ============================================================================
# AUTHOR MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """Create a new author"""
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=List[schemas.Author])
def list_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get list of all authors with pagination"""
    return crud.get_authors(db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """Get author by ID"""
    author = crud.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@app.get("/authors/search/{query}", response_model=List[schemas.Author])
def search_authors(query: str = Path(..., min_length=1), db: Session = Depends(get_db)):
    """Search authors by name"""
    return crud.search_authors(db, query=query)

# ============================================================================
# USER MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new library user"""
    # Check if user with same user_id or email already exists
    if crud.get_user_by_user_id(db, user.user_id):
        raise HTTPException(status_code=400, detail="User ID already registered")
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get list of all users with pagination"""
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """Get user by ID"""
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/lookup/{user_id_str}", response_model=schemas.User)
def get_user_by_user_id(user_id_str: str = Path(...), db: Session = Depends(get_db)):
    """Get user by user ID string"""
    user = crud.get_user_by_user_id(db, user_id=user_id_str)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int = Path(..., ge=1),
    user_update: schemas.UserUpdate = None,
    db: Session = Depends(get_db)
):
    """Update user information"""
    user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ============================================================================
# CHECKOUT MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/checkouts/", response_model=schemas.Checkout)
def create_checkout(checkout: schemas.CheckoutCreate, db: Session = Depends(get_db)):
    """Check out a book to a user"""
    db_checkout = crud.create_checkout(db=db, checkout=checkout)
    if db_checkout is None:
        raise HTTPException(
            status_code=400, 
            detail="Cannot checkout book. Book may be unavailable or user has reached checkout limit."
        )
    return db_checkout

@app.put("/checkouts/{checkout_id}/return")
def return_book(
    checkout_id: int = Path(..., ge=1),
    return_condition: str = Query("good", regex="^(good|fair|damaged|lost)$"),
    db: Session = Depends(get_db)
):
    """Return a book"""
    checkout = crud.return_book(db, checkout_id=checkout_id, return_condition=return_condition)
    if checkout is None:
        raise HTTPException(status_code=404, detail="Checkout not found or already returned")
    return {"message": "Book returned successfully", "checkout": checkout}

@app.put("/checkouts/{checkout_id}/renew", response_model=schemas.Checkout)
def renew_checkout(checkout_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """Renew a book checkout"""
    checkout = crud.renew_checkout(db, checkout_id=checkout_id)
    if checkout is None:
        raise HTTPException(
            status_code=400, 
            detail="Cannot renew checkout. May have reached renewal limit or book is reserved."
        )
    return checkout

@app.get("/users/{user_id}/checkouts", response_model=List[schemas.Checkout])
def get_user_checkouts(
    user_id: int = Path(..., ge=1),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get user's checkouts"""
    if not crud.get_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_user_checkouts(db, user_id=user_id, active_only=active_only)

@app.get("/checkouts/overdue", response_model=List[schemas.Checkout])
def get_overdue_books(db: Session = Depends(get_db)):
    """Get all overdue books"""
    return crud.get_overdue_books(db)

# ============================================================================
# RESERVATION MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/reservations/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    """Create a book reservation"""
    db_reservation = crud.create_reservation(db=db, reservation=reservation)
    if db_reservation is None:
        raise HTTPException(
            status_code=400, 
            detail="Cannot create reservation. Book may be available or user already has a reservation."
        )
    return db_reservation

@app.get("/users/{user_id}/reservations", response_model=List[schemas.Reservation])
def get_user_reservations(
    user_id: int = Path(..., ge=1),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get user's reservations"""
    if not crud.get_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_user_reservations(db, user_id=user_id, active_only=active_only)

# ============================================================================
# REVIEW MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/reviews/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    """Create a book review"""
    # Validate user and book exist
    if not crud.get_user(db, review.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if not crud.get_book(db, review.book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    
    return crud.create_review(db=db, review=review)

@app.get("/books/{book_id}/reviews", response_model=List[schemas.Review])
def get_book_reviews(
    book_id: int = Path(..., ge=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get reviews for a book"""
    if not crud.get_book(db, book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.get_book_reviews(db, book_id=book_id, skip=skip, limit=limit)

# ============================================================================
# ANALYTICS AND DASHBOARD ENDPOINTS
# ============================================================================

@app.get("/analytics/dashboard", response_model=schemas.LibraryDashboard)
def get_library_dashboard(db: Session = Depends(get_db)):
    """Get comprehensive library dashboard analytics"""
    return crud.get_dashboard_analytics(db)

@app.get("/analytics/books")
def get_book_analytics(db: Session = Depends(get_db)):
    """Get detailed book analytics"""
    total_books = db.query(models.Book).count()
    available_books = db.query(models.Book).filter(models.Book.status == "available").count()
    checked_out_books = db.query(models.Book).filter(models.Book.status == "checked_out").count()
    
    # Format distribution
    format_stats = db.query(
        models.Book.format_type,
        func.count(models.Book.id)
    ).group_by(models.Book.format_type).all()
    
    # Language distribution
    language_stats = db.query(
        models.Book.language,
        func.count(models.Book.id)
    ).group_by(models.Book.language).all()
    
    return {
        "total_books": total_books,
        "available_books": available_books,
        "checked_out_books": checked_out_books,
        "format_distribution": {format_type: count for format_type, count in format_stats},
        "language_distribution": {language: count for language, count in language_stats},
        "availability_rate": (available_books / total_books * 100) if total_books > 0 else 0
    }

@app.get("/analytics/circulation")
def get_circulation_analytics(db: Session = Depends(get_db)):
    """Get circulation analytics"""
    from sqlalchemy import func
    
    total_checkouts = db.query(models.Checkout).count()
    active_checkouts = db.query(models.Checkout).filter(models.Checkout.checkout_status == "active").count()
    overdue_checkouts = crud.get_overdue_books(db)
    total_reservations = db.query(models.Reservation).filter(models.Reservation.status == "active").count()
    
    # Most popular books
    popular_books = db.query(models.Book).order_by(models.Book.total_checkouts.desc()).limit(10).all()
    
    return {
        "total_checkouts": total_checkouts,
        "active_checkouts": active_checkouts,
        "overdue_count": len(overdue_checkouts),
        "total_reservations": total_reservations,
        "overdue_rate": (len(overdue_checkouts) / active_checkouts * 100) if active_checkouts > 0 else 0,
        "most_popular_books": [
            {
                "id": book.id,
                "title": book.title,
                "checkouts": book.total_checkouts,
                "rating": book.average_rating
            }
            for book in popular_books
        ]
    }

@app.get("/analytics/users")
def get_user_analytics(db: Session = Depends(get_db)):
    """Get user analytics"""
    from sqlalchemy import func
    
    total_users = db.query(models.User).count()
    active_users = db.query(models.User).filter(models.User.membership_status == "active").count()
    
    # Membership type distribution
    membership_stats = db.query(
        models.User.membership_type,
        func.count(models.User.id)
    ).group_by(models.User.membership_type).all()
    
    # Users with current checkouts
    users_with_checkouts = db.query(models.User).filter(models.User.current_checkouts > 0).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "membership_distribution": {membership: count for membership, count in membership_stats},
        "users_with_active_checkouts": users_with_checkouts,
        "utilization_rate": (users_with_checkouts / active_users * 100) if active_users > 0 else 0
    }

# ============================================================================
# AI AND RECOMMENDATION ENDPOINTS
# ============================================================================

@app.post("/ai/recommendations", response_model=List[schemas.RecommendationResult])
def get_book_recommendations(
    recommendation_request: schemas.BookRecommendation,
    db: Session = Depends(get_db)
):
    """Get AI-powered book recommendations"""
    # This is a placeholder for AI recommendation logic
    # In a real implementation, this would use ML models
    
    if recommendation_request.recommendation_type == "popular":
        popular_books = crud.get_popular_books(db, recommendation_request.limit)
        return [
            schemas.RecommendationResult(
                book_id=book.id,
                title=book.title,
                authors=["Unknown Author"],  # TODO: Get actual authors
                score=book.popularity_score,
                reason="Popular among other readers",
                similarity_factors=["high_rating", "frequent_checkouts"]
            )
            for book in popular_books
        ]
    
    # TODO: Implement other recommendation types
    return []

@app.post("/ai/analyze-book", response_model=schemas.BookAnalysisResult)
def analyze_book(
    analysis_request: schemas.BookAnalysisRequest,
    db: Session = Depends(get_db)
):
    """AI analysis of book content"""
    book = crud.get_book(db, analysis_request.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Placeholder AI analysis
    # In a real implementation, this would use NLP models
    
    return schemas.BookAnalysisResult(
        book_id=book.id,
        analysis_type=analysis_request.analysis_type,
        content_tags=["fiction", "adventure", "coming-of-age"] if book.content_tags else [],
        themes=["friendship", "growth", "adventure"] if not book.theme_keywords else book.theme_keywords,
        sentiment_score=book.sentiment_score or 0.7,
        complexity_score=book.complexity_score or 6.5,
        reading_time_estimate=book.page_count * 2 / 60 if book.page_count else 5.0,  # Estimate 2 minutes per page
        target_audience=[book.reading_level] if book.reading_level else ["General"],
        similar_books=book.similar_books or []
    )

@app.get("/users/{user_id}/reading-insights", response_model=schemas.ReadingInsights)
def get_reading_insights(user_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """Get AI-powered reading insights for a user"""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's checkout history
    checkouts = crud.get_user_checkouts(db, user_id, active_only=False)
    returned_checkouts = [c for c in checkouts if c.checkout_status == "returned"]
    
    # Calculate basic stats
    total_books_read = len(returned_checkouts)
    total_pages_read = sum(
        crud.get_book(db, c.book_id).page_count or 0 
        for c in returned_checkouts
    )
    total_reading_time = sum(c.actual_reading_time or 0 for c in returned_checkouts)
    
    return schemas.ReadingInsights(
        user_id=user_id,
        total_books_read=total_books_read,
        total_pages_read=total_pages_read,
        total_reading_time=total_reading_time,
        average_rating_given=0.0,  # TODO: Calculate from reviews
        favorite_genres=user.preferred_genres or [],
        reading_speed_wpm=user.reading_speed_wpm or 250,
        reading_consistency="weekly",  # TODO: Calculate from patterns
        reading_goals_progress=user.reading_goals or {},
        recommendations=[]  # TODO: Generate personalized recommendations
    )

# ============================================================================
# DATA IMPORT ENDPOINTS
# ============================================================================

class BulkImportData(BaseModel):
    data_type: str  # "books", "authors", "users"
    data: str  # CSV or JSON data

@app.post("/import/bulk")
def bulk_import_data(import_data: BulkImportData, db: Session = Depends(get_db)):
    """Bulk import data from CSV/JSON"""
    # This is a placeholder for bulk import functionality
    # In a real implementation, this would parse CSV/JSON and create records
    
    return {
        "message": f"Bulk import initiated for {import_data.data_type}",
        "status": "processing",
        "imported_count": 0,
        "errors": []
    }

# ============================================================================
# SYSTEM MANAGEMENT ENDPOINTS
# ============================================================================

@app.get("/system/stats")
def get_system_stats(db: Session = Depends(get_db)):
    """Get system statistics"""
    from sqlalchemy import func
    
    # Database stats
    total_books = db.query(models.Book).count()
    total_users = db.query(models.User).count()
    total_checkouts = db.query(models.Checkout).count()
    total_reviews = db.query(models.Review).count()
    
    # Recent activity
    recent_checkouts = db.query(models.Checkout).filter(
        models.Checkout.checkout_date >= datetime.utcnow() - timedelta(days=7)
    ).count()
    
    recent_returns = db.query(models.Checkout).filter(
        and_(
            models.Checkout.return_date >= datetime.utcnow() - timedelta(days=7),
            models.Checkout.checkout_status == "returned"
        )
    ).count()
    
    return {
        "database_stats": {
            "total_books": total_books,
            "total_users": total_users,
            "total_checkouts": total_checkouts,
            "total_reviews": total_reviews
        },
        "recent_activity": {
            "checkouts_this_week": recent_checkouts,
            "returns_this_week": recent_returns
        },
        "system_health": "healthy",
        "uptime": "99.9%",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)