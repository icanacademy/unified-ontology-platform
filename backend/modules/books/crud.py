from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, asc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import models, schemas

# ============================================================================
# BOOK OPERATIONS
# ============================================================================

def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    """Create a new book"""
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    """Get book by ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_book_by_isbn(db: Session, isbn: str) -> Optional[models.Book]:
    """Get book by ISBN (10 or 13)"""
    return db.query(models.Book).filter(
        or_(models.Book.isbn_10 == isbn, models.Book.isbn_13 == isbn)
    ).first()

def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    """Get all books with pagination"""
    return db.query(models.Book).offset(skip).limit(limit).all()

def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate) -> Optional[models.Book]:
    """Update book information"""
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    
    update_data = book_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    db_book.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> bool:
    """Delete a book"""
    db_book = get_book(db, book_id)
    if not db_book:
        return False
    
    db.delete(db_book)
    db.commit()
    return True

def search_books(db: Session, search_params: schemas.BookSearch) -> List[models.Book]:
    """Advanced book search"""
    query = db.query(models.Book)
    
    # Text search across multiple fields
    if search_params.query:
        search_term = f"%{search_params.query}%"
        query = query.filter(
            or_(
                models.Book.title.contains(search_term),
                models.Book.subtitle.contains(search_term),
                models.Book.description.contains(search_term)
            )
        )
    
    # Specific field filters
    if search_params.title:
        query = query.filter(models.Book.title.contains(search_params.title))
    
    if search_params.isbn:
        query = query.filter(
            or_(
                models.Book.isbn_10 == search_params.isbn,
                models.Book.isbn_13 == search_params.isbn
            )
        )
    
    if search_params.format_type:
        query = query.filter(models.Book.format_type == search_params.format_type)
    
    if search_params.reading_level:
        query = query.filter(models.Book.reading_level == search_params.reading_level)
    
    if search_params.availability_status:
        query = query.filter(models.Book.status == search_params.availability_status)
    
    if search_params.language:
        query = query.filter(models.Book.language == search_params.language)
    
    # Date range filters
    if search_params.publication_year_from:
        start_date = datetime(search_params.publication_year_from, 1, 1)
        query = query.filter(models.Book.publication_date >= start_date)
    
    if search_params.publication_year_to:
        end_date = datetime(search_params.publication_year_to, 12, 31)
        query = query.filter(models.Book.publication_date <= end_date)
    
    # Page count range
    if search_params.page_count_min:
        query = query.filter(models.Book.page_count >= search_params.page_count_min)
    
    if search_params.page_count_max:
        query = query.filter(models.Book.page_count <= search_params.page_count_max)
    
    # Rating filter
    if search_params.rating_min:
        query = query.filter(models.Book.average_rating >= search_params.rating_min)
    
    # Sorting
    if search_params.sort_by == "title":
        order = asc(models.Book.title) if search_params.sort_order == "asc" else desc(models.Book.title)
    elif search_params.sort_by == "publication_date":
        order = asc(models.Book.publication_date) if search_params.sort_order == "asc" else desc(models.Book.publication_date)
    elif search_params.sort_by == "rating":
        order = asc(models.Book.average_rating) if search_params.sort_order == "asc" else desc(models.Book.average_rating)
    else:  # relevance or popularity
        order = desc(models.Book.popularity_score)
    
    query = query.order_by(order)
    
    # Pagination
    return query.offset(search_params.offset).limit(search_params.limit).all()

def get_popular_books(db: Session, limit: int = 10) -> List[models.Book]:
    """Get most popular books"""
    return db.query(models.Book).order_by(desc(models.Book.popularity_score)).limit(limit).all()

def get_recently_added_books(db: Session, limit: int = 10) -> List[models.Book]:
    """Get recently added books"""
    return db.query(models.Book).order_by(desc(models.Book.created_at)).limit(limit).all()

# ============================================================================
# AUTHOR OPERATIONS
# ============================================================================

def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    """Create a new author"""
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    """Get author by ID"""
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Author]:
    """Get all authors with pagination"""
    return db.query(models.Author).offset(skip).limit(limit).all()

def search_authors(db: Session, query: str) -> List[models.Author]:
    """Search authors by name"""
    search_term = f"%{query}%"
    return db.query(models.Author).filter(
        or_(
            models.Author.first_name.contains(search_term),
            models.Author.last_name.contains(search_term)
        )
    ).all()

# ============================================================================
# USER OPERATIONS
# ============================================================================

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    db_user = models.User(**user.dict())
    db_user.membership_start_date = datetime.utcnow()
    # Set expiry date to 1 year from now
    db_user.membership_expiry_date = datetime.utcnow() + timedelta(days=365)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Get user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_user_id(db: Session, user_id: str) -> Optional[models.User]:
    """Get user by user_id string"""
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Get all users with pagination"""
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    """Update user information"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# ============================================================================
# CHECKOUT OPERATIONS
# ============================================================================

def create_checkout(db: Session, checkout: schemas.CheckoutCreate) -> Optional[models.Checkout]:
    """Create a new book checkout"""
    # Check if book is available
    book = get_book(db, checkout.book_id)
    if not book or book.status != "available":
        return None
    
    # Check user's checkout limit
    user = get_user(db, checkout.user_id)
    if not user or user.current_checkouts >= user.max_concurrent_books:
        return None
    
    # Calculate due date
    due_date = checkout.due_date or datetime.utcnow() + timedelta(days=book.checkout_period_days)
    
    # Create checkout
    db_checkout = models.Checkout(
        user_id=checkout.user_id,
        book_id=checkout.book_id,
        due_date=due_date,
        max_renewals=checkout.max_renewals,
        checkout_method=checkout.checkout_method,
        properties=checkout.properties
    )
    
    # Update book and user status
    book.status = "checked_out"
    book.total_checkouts += 1
    user.current_checkouts += 1
    
    db.add(db_checkout)
    db.commit()
    db.refresh(db_checkout)
    return db_checkout

def return_book(db: Session, checkout_id: int, return_condition: str = "good") -> Optional[models.Checkout]:
    """Return a book"""
    checkout = db.query(models.Checkout).filter(models.Checkout.id == checkout_id).first()
    if not checkout or checkout.checkout_status != "active":
        return None
    
    # Update checkout
    checkout.return_date = datetime.utcnow()
    checkout.checkout_status = "returned"
    checkout.return_condition = return_condition
    checkout.return_method = "in_person"  # Default
    
    # Calculate fines if overdue
    if datetime.utcnow() > checkout.due_date:
        overdue_days = (datetime.utcnow() - checkout.due_date).days
        checkout.overdue_fine = overdue_days * 0.25  # $0.25 per day
    
    # Update book and user status
    book = get_book(db, checkout.book_id)
    user = get_user(db, checkout.user_id)
    
    if book:
        book.status = "available"
    
    if user:
        user.current_checkouts = max(0, user.current_checkouts - 1)
        user.total_fines += checkout.overdue_fine
    
    db.commit()
    db.refresh(checkout)
    return checkout

def get_user_checkouts(db: Session, user_id: int, active_only: bool = True) -> List[models.Checkout]:
    """Get user's checkouts"""
    query = db.query(models.Checkout).filter(models.Checkout.user_id == user_id)
    if active_only:
        query = query.filter(models.Checkout.checkout_status == "active")
    return query.order_by(desc(models.Checkout.checkout_date)).all()

def get_overdue_books(db: Session) -> List[models.Checkout]:
    """Get all overdue books"""
    return db.query(models.Checkout).filter(
        and_(
            models.Checkout.checkout_status == "active",
            models.Checkout.due_date < datetime.utcnow()
        )
    ).all()

def renew_checkout(db: Session, checkout_id: int) -> Optional[models.Checkout]:
    """Renew a book checkout"""
    checkout = db.query(models.Checkout).filter(models.Checkout.id == checkout_id).first()
    if not checkout or checkout.checkout_status != "active":
        return None
    
    if checkout.renewal_count >= checkout.max_renewals:
        return None
    
    # Check if book has reservations
    book = get_book(db, checkout.book_id)
    if book and book.current_reservations > 0:
        return None
    
    # Renew checkout
    checkout.renewal_count += 1
    checkout.due_date = datetime.utcnow() + timedelta(days=book.checkout_period_days)
    
    db.commit()
    db.refresh(checkout)
    return checkout

# ============================================================================
# RESERVATION OPERATIONS
# ============================================================================

def create_reservation(db: Session, reservation: schemas.ReservationCreate) -> Optional[models.Reservation]:
    """Create a book reservation"""
    # Check if book exists and is not available
    book = get_book(db, reservation.book_id)
    if not book or book.status == "available":
        return None
    
    # Check if user already has a reservation for this book
    existing = db.query(models.Reservation).filter(
        and_(
            models.Reservation.user_id == reservation.user_id,
            models.Reservation.book_id == reservation.book_id,
            models.Reservation.status == "active"
        )
    ).first()
    
    if existing:
        return None
    
    # Create reservation
    expiry_date = reservation.expiry_date or datetime.utcnow() + timedelta(days=30)
    
    db_reservation = models.Reservation(
        user_id=reservation.user_id,
        book_id=reservation.book_id,
        expiry_date=expiry_date,
        priority_level=reservation.priority_level,
        properties=reservation.properties
    )
    
    # Update book reservation count
    book.current_reservations += 1
    
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_user_reservations(db: Session, user_id: int, active_only: bool = True) -> List[models.Reservation]:
    """Get user's reservations"""
    query = db.query(models.Reservation).filter(models.Reservation.user_id == user_id)
    if active_only:
        query = query.filter(models.Reservation.status == "active")
    return query.order_by(desc(models.Reservation.reservation_date)).all()

# ============================================================================
# REVIEW OPERATIONS
# ============================================================================

def create_review(db: Session, review: schemas.ReviewCreate) -> models.Review:
    """Create a book review"""
    # Check if user has checked out this book (for verified reader status)
    checkout_exists = db.query(models.Checkout).filter(
        and_(
            models.Checkout.user_id == review.user_id,
            models.Checkout.book_id == review.book_id,
            models.Checkout.checkout_status == "returned"
        )
    ).first()
    
    db_review = models.Review(**review.dict())
    db_review.is_verified_reader = checkout_exists is not None
    
    db.add(db_review)
    db.commit()
    
    # Update book's average rating
    update_book_rating(db, review.book_id)
    
    db.refresh(db_review)
    return db_review

def get_book_reviews(db: Session, book_id: int, skip: int = 0, limit: int = 20) -> List[models.Review]:
    """Get reviews for a book"""
    return db.query(models.Review).filter(
        and_(
            models.Review.book_id == book_id,
            models.Review.is_approved == True
        )
    ).order_by(desc(models.Review.created_at)).offset(skip).limit(limit).all()

def update_book_rating(db: Session, book_id: int):
    """Update book's average rating based on reviews"""
    result = db.query(func.avg(models.Review.rating), func.count(models.Review.id)).filter(
        and_(
            models.Review.book_id == book_id,
            models.Review.is_approved == True
        )
    ).first()
    
    book = get_book(db, book_id)
    if book and result[0]:
        book.average_rating = float(result[0])
        book.total_reviews = result[1]
        db.commit()

# ============================================================================
# ANALYTICS OPERATIONS
# ============================================================================

def get_dashboard_analytics(db: Session) -> schemas.LibraryDashboard:
    """Get comprehensive library dashboard analytics"""
    
    # Book Analytics
    total_books = db.query(models.Book).count()
    total_authors = db.query(models.Author).count()
    total_genres = db.query(models.Genre).count()
    
    # Popular books (by checkout count)
    popular_books = db.query(models.Book).order_by(desc(models.Book.total_checkouts)).limit(5).all()
    popular_books_data = [
        {
            "id": book.id,
            "title": book.title,
            "total_checkouts": book.total_checkouts,
            "average_rating": book.average_rating
        }
        for book in popular_books
    ]
    
    # Recent additions
    recent_books = get_recently_added_books(db, 5)
    recent_books_data = [
        {
            "id": book.id,
            "title": book.title,
            "created_at": book.created_at.isoformat(),
            "format_type": book.format_type
        }
        for book in recent_books
    ]
    
    # Circulation stats
    total_checkouts = db.query(models.Checkout).count()
    active_checkouts = db.query(models.Checkout).filter(models.Checkout.checkout_status == "active").count()
    overdue_count = db.query(models.Checkout).filter(
        and_(
            models.Checkout.checkout_status == "active",
            models.Checkout.due_date < datetime.utcnow()
        )
    ).count()
    
    # User Analytics
    total_users = db.query(models.User).count()
    active_users = db.query(models.User).filter(models.User.membership_status == "active").count()
    
    # Format distribution
    format_counts = db.query(models.Book.format_type, func.count(models.Book.id)).group_by(models.Book.format_type).all()
    digital_vs_physical = {
        "physical": sum(count for format_type, count in format_counts if format_type in ["hardcover", "paperback"]),
        "digital": sum(count for format_type, count in format_counts if format_type in ["ebook", "audiobook"])
    }
    
    # Reading level distribution
    level_counts = db.query(models.Book.reading_level, func.count(models.Book.id)).group_by(models.Book.reading_level).all()
    reading_level_distribution = {level or "Unknown": count for level, count in level_counts}
    
    # Condition distribution
    condition_counts = db.query(models.Book.condition, func.count(models.Book.id)).group_by(models.Book.condition).all()
    condition_distribution = {condition: count for condition, count in condition_counts}
    
    book_analytics = schemas.BookAnalytics(
        total_books=total_books,
        total_authors=total_authors,
        total_genres=total_genres,
        most_popular_books=popular_books_data,
        most_popular_authors=[],  # TODO: Implement
        most_popular_genres=[],   # TODO: Implement
        recent_additions=recent_books_data,
        circulation_stats={
            "total_checkouts": total_checkouts,
            "active_checkouts": active_checkouts,
            "overdue_books": overdue_count
        },
        digital_vs_physical=digital_vs_physical,
        reading_level_distribution=reading_level_distribution,
        condition_distribution=condition_distribution
    )
    
    user_analytics = schemas.UserAnalytics(
        total_users=total_users,
        active_users=active_users,
        new_registrations_this_month=0,  # TODO: Implement
        membership_distribution={},       # TODO: Implement
        age_group_distribution={},        # TODO: Implement
        reading_preferences={},           # TODO: Implement
        geographic_distribution={},       # TODO: Implement
        average_books_per_user=0.0       # TODO: Implement
    )
    
    circulation_analytics = schemas.CirculationAnalytics(
        total_checkouts=total_checkouts,
        total_returns=db.query(models.Checkout).filter(models.Checkout.checkout_status == "returned").count(),
        active_checkouts=active_checkouts,
        overdue_books=overdue_count,
        total_reservations=db.query(models.Reservation).filter(models.Reservation.status == "active").count(),
        average_checkout_duration=14.0,   # TODO: Calculate actual average
        most_borrowed_books=popular_books_data,
        checkout_trends={},               # TODO: Implement
        return_rate=0.95,                 # TODO: Calculate
        renewal_rate=0.30                 # TODO: Calculate
    )
    
    return schemas.LibraryDashboard(
        book_analytics=book_analytics,
        user_analytics=user_analytics,
        circulation_analytics=circulation_analytics,
        recent_activity=[],               # TODO: Implement
        upcoming_events=[],               # TODO: Implement
        system_alerts=[],                 # TODO: Implement
        performance_metrics={}            # TODO: Implement
    )