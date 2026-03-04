from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta
from . import crud, models, schemas
from .database import SessionLocal, engine
from pydantic import BaseModel

# Create database tables
models.Base.metadata.create_all(bind=engine)

router = APIRouter()

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

@router.get("/")
async def books_root():
    return {
        "message": "Books & Library Management Platform API",
        "version": "1.0.0",
        "description": "AI-Powered Comprehensive Library System"
    }

@router.get("/health")
async def books_health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# ============================================================================
# BOOK MANAGEMENT ENDPOINTS
# ============================================================================

@router.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Create a new book"""
    # Check if book with same ISBN already exists
    if book.isbn_10 and crud.get_book_by_isbn(db, book.isbn_10):
        raise HTTPException(status_code=400, detail="Book with this ISBN-10 already exists")
    if book.isbn_13 and crud.get_book_by_isbn(db, book.isbn_13):
        raise HTTPException(status_code=400, detail="Book with this ISBN-13 already exists")
    
    return crud.create_book(db=db, book=book)

@router.get("/books/", response_model=List[schemas.Book])
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get list of all books with pagination"""
    return crud.get_books(db, skip=skip, limit=limit)

@router.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """Get book by ID"""
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/books/{book_id}", response_model=schemas.Book)
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

@router.delete("/books/{book_id}")
def delete_book(book_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """Delete a book"""
    if not crud.delete_book(db, book_id=book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

@router.post("/books/search", response_model=List[schemas.Book])
def search_books(search_params: schemas.BookSearch, db: Session = Depends(get_db)):
    """Advanced book search"""
    return crud.search_books(db, search_params)

@router.get("/books/popular/trending", response_model=List[schemas.Book])
def get_popular_books(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    """Get most popular books"""
    return crud.get_popular_books(db, limit=limit)

@router.get("/books/recent/additions", response_model=List[schemas.Book])
def get_recent_books(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    """Get recently added books"""
    return crud.get_recently_added_books(db, limit=limit)

@router.get("/books/isbn/{isbn}", response_model=schemas.Book)
def get_book_by_isbn(isbn: str = Path(..., min_length=10, max_length=17), db: Session = Depends(get_db)):
    """Get book by ISBN"""
    book = crud.get_book_by_isbn(db, isbn=isbn)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# ============================================================================
# AUTHOR MANAGEMENT ENDPOINTS
# ============================================================================

@router.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """Create a new author"""
    return crud.create_author(db=db, author=author)

@router.get("/authors/", response_model=List[schemas.Author])
def list_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get list of all authors with pagination"""
    return crud.get_authors(db, skip=skip, limit=limit)

@router.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """Get author by ID"""
    author = crud.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.get("/authors/search/{query}", response_model=List[schemas.Author])
def search_authors(query: str = Path(..., min_length=1), db: Session = Depends(get_db)):
    """Search authors by name"""
    return crud.search_authors(db, query=query)

# ============================================================================
# USER MANAGEMENT ENDPOINTS
# ============================================================================

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new library user"""
    # Check if user with same user_id or email already exists
    if crud.get_user_by_user_id(db, user.user_id):
        raise HTTPException(status_code=400, detail="User ID already registered")
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_user(db=db, user=user)

@router.get("/users/", response_model=List[schemas.User])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get list of all users with pagination"""
    return crud.get_users(db, skip=skip, limit=limit)

@router.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """Get user by ID"""
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/lookup/{user_id_str}", response_model=schemas.User)
def get_user_by_user_id(user_id_str: str = Path(...), db: Session = Depends(get_db)):
    """Get user by user ID string"""
    user = crud.get_user_by_user_id(db, user_id=user_id_str)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=schemas.User)
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

@router.post("/checkouts/", response_model=schemas.Checkout)
def create_checkout(checkout: schemas.CheckoutCreate, db: Session = Depends(get_db)):
    """Check out a book to a user"""
    db_checkout = crud.create_checkout(db=db, checkout=checkout)
    if db_checkout is None:
        raise HTTPException(
            status_code=400, 
            detail="Cannot checkout book. Book may be unavailable or user has reached checkout limit."
        )
    return db_checkout

@router.put("/checkouts/{checkout_id}/return")
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

@router.put("/checkouts/{checkout_id}/renew", response_model=schemas.Checkout)
def renew_checkout(checkout_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """Renew a book checkout"""
    checkout = crud.renew_checkout(db, checkout_id=checkout_id)
    if checkout is None:
        raise HTTPException(
            status_code=400, 
            detail="Cannot renew checkout. May have reached renewal limit or book is reserved."
        )
    return checkout

@router.get("/users/{user_id}/checkouts", response_model=List[schemas.Checkout])
def get_user_checkouts(
    user_id: int = Path(..., ge=1),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get user's checkouts"""
    if not crud.get_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_user_checkouts(db, user_id=user_id, active_only=active_only)

@router.get("/checkouts/overdue", response_model=List[schemas.Checkout])
def get_overdue_books(db: Session = Depends(get_db)):
    """Get all overdue books"""
    return crud.get_overdue_books(db)

# ============================================================================
# ANALYTICS AND DASHBOARD ENDPOINTS
# ============================================================================

@router.get("/analytics/dashboard", response_model=schemas.LibraryDashboard)
def get_library_dashboard(db: Session = Depends(get_db)):
    """Get comprehensive library dashboard analytics"""
    return crud.get_dashboard_analytics(db)