from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

# Base schemas
class BookBase(BaseModel):
    title: str
    subtitle: Optional[str] = None
    isbn_10: Optional[str] = None
    isbn_13: Optional[str] = None
    publication_date: Optional[datetime] = None
    publisher: Optional[str] = None
    edition: Optional[str] = None
    language: str = "English"
    page_count: Optional[int] = None
    format_type: Optional[str] = None
    dimensions: Optional[str] = None
    weight: Optional[float] = None
    description: Optional[str] = None
    table_of_contents: Optional[str] = None
    excerpt: Optional[str] = None
    age_rating: Optional[str] = None
    reading_level: Optional[str] = None
    ebook_available: bool = False
    audiobook_available: bool = False
    digital_format: Optional[List[str]] = []
    ebook_file_size: Optional[float] = None
    audiobook_duration: Optional[float] = None
    narrator: Optional[str] = None
    acquisition_date: Optional[datetime] = None
    acquisition_method: Optional[str] = None
    acquisition_cost: Optional[float] = None
    supplier: Optional[str] = None
    location_code: Optional[str] = None
    barcode: Optional[str] = None
    dewey_decimal: Optional[str] = None
    library_of_congress: Optional[str] = None
    condition: str = "Good"
    replacement_cost: Optional[float] = None
    status: str = "available"
    is_reference_only: bool = False
    is_popular_demand: bool = False
    checkout_period_days: int = 14
    content_tags: Optional[List[str]] = []
    complexity_score: Optional[float] = None
    sentiment_score: Optional[float] = None
    theme_keywords: Optional[List[str]] = []
    properties: Optional[Dict[str, Any]] = {}

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    isbn_10: Optional[str] = None
    isbn_13: Optional[str] = None
    publication_date: Optional[datetime] = None
    publisher: Optional[str] = None
    edition: Optional[str] = None
    language: Optional[str] = None
    page_count: Optional[int] = None
    format_type: Optional[str] = None
    description: Optional[str] = None
    age_rating: Optional[str] = None
    reading_level: Optional[str] = None
    ebook_available: Optional[bool] = None
    audiobook_available: Optional[bool] = None
    location_code: Optional[str] = None
    condition: Optional[str] = None
    status: Optional[str] = None
    is_reference_only: Optional[bool] = None

class Book(BookBase):
    id: int
    total_checkouts: int
    current_reservations: int
    average_rating: float
    total_reviews: int
    popularity_score: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Author schemas
class AuthorBase(BaseModel):
    first_name: Optional[str] = None
    last_name: str
    middle_name: Optional[str] = None
    pen_names: Optional[List[str]] = []
    birth_date: Optional[datetime] = None
    death_date: Optional[datetime] = None
    nationality: Optional[str] = None
    biography: Optional[str] = None
    education: Optional[List[Dict[str, Any]]] = []
    awards: Optional[List[str]] = []
    website: Optional[str] = None
    social_media: Optional[Dict[str, str]] = {}
    properties: Optional[Dict[str, Any]] = {}

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    total_books: int
    first_publication_date: Optional[datetime]
    latest_publication_date: Optional[datetime]
    average_book_rating: float
    total_book_sales: int
    popularity_trend: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Genre schemas
class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_genre_id: Optional[int] = None
    properties: Optional[Dict[str, Any]] = {}

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int
    total_books: int
    popularity_score: float
    average_rating: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    membership_type: str = "standard"
    membership_start_date: Optional[datetime] = None
    membership_expiry_date: Optional[datetime] = None
    max_concurrent_books: int = 5
    preferred_genres: Optional[List[int]] = []
    preferred_formats: Optional[List[str]] = []
    reading_goals: Optional[Dict[str, Any]] = {}
    reading_challenges: Optional[List[Dict[str, Any]]] = []
    privacy_settings: Optional[Dict[str, Any]] = {}
    notification_preferences: Optional[Dict[str, Any]] = {}
    reading_history_public: bool = False
    properties: Optional[Dict[str, Any]] = {}

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    membership_type: Optional[str] = None
    max_concurrent_books: Optional[int] = None
    preferred_genres: Optional[List[int]] = None
    preferred_formats: Optional[List[str]] = None
    reading_goals: Optional[Dict[str, Any]] = None

class User(UserBase):
    id: int
    membership_status: str
    current_checkouts: int
    overdue_books: int
    total_fines: float
    reading_speed_wpm: Optional[float]
    reading_comprehension_score: Optional[float]
    favorite_topics: Optional[List[str]]
    reading_patterns: Optional[Dict[str, Any]]
    personality_profile: Optional[Dict[str, Any]]
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

# Checkout schemas
class CheckoutBase(BaseModel):
    user_id: int
    book_id: int
    due_date: Optional[datetime] = None
    max_renewals: int = 2
    checkout_method: Optional[str] = "in_person"
    properties: Optional[Dict[str, Any]] = {}

class CheckoutCreate(CheckoutBase):
    pass

class Checkout(CheckoutBase):
    id: int
    checkout_date: datetime
    return_date: Optional[datetime]
    renewal_count: int
    checkout_status: str
    return_method: Optional[str]
    return_condition: Optional[str]
    overdue_fine: float
    damage_fee: float
    replacement_fee: float
    fine_paid: bool
    actual_reading_time: Optional[float]
    completion_percentage: Optional[float]
    user_rating: Optional[float]
    checkout_notes: Optional[str]
    return_notes: Optional[str]
    
    class Config:
        from_attributes = True

# Reservation schemas
class ReservationBase(BaseModel):
    user_id: int
    book_id: int
    expiry_date: Optional[datetime] = None
    priority_level: int = 1
    properties: Optional[Dict[str, Any]] = {}

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    reservation_date: datetime
    notification_sent: bool
    pickup_by_date: Optional[datetime]
    status: str
    fulfilled_date: Optional[datetime]
    pickup_date: Optional[datetime]
    
    class Config:
        from_attributes = True

# Review schemas
class ReviewBase(BaseModel):
    user_id: int
    book_id: int
    rating: int  # 1-5
    title: Optional[str] = None
    review_text: Optional[str] = None
    reading_date: Optional[datetime] = None
    is_spoiler: bool = False
    properties: Optional[Dict[str, Any]] = {}

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    is_verified_reader: bool
    helpful_votes: int
    total_votes: int
    sentiment_score: Optional[float]
    content_tags: Optional[List[str]]
    reading_experience: Optional[Dict[str, Any]]
    is_approved: bool
    moderation_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Reading Session schemas
class ReadingSessionBase(BaseModel):
    user_id: int
    book_id: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    start_page: Optional[int] = None
    end_page: Optional[int] = None
    pages_read: Optional[int] = None
    completion_percentage: Optional[float] = None
    reading_location: Optional[str] = None
    reading_format: Optional[str] = None
    device_used: Optional[str] = None
    reading_speed_wpm: Optional[float] = None
    comprehension_notes: Optional[str] = None
    difficulty_rating: Optional[int] = None
    enjoyment_rating: Optional[int] = None
    interruptions: int = 0
    environmental_rating: Optional[int] = None
    properties: Optional[Dict[str, Any]] = {}

class ReadingSessionCreate(ReadingSessionBase):
    pass

class ReadingSession(ReadingSessionBase):
    id: int
    
    class Config:
        from_attributes = True

# Collection schemas
class CollectionBase(BaseModel):
    name: str
    description: Optional[str] = None
    collection_type: str = "thematic"
    curator_name: Optional[str] = None
    creation_purpose: Optional[str] = None
    target_audience: Optional[List[str]] = []
    is_public: bool = True
    is_featured: bool = False
    display_order: int = 0
    properties: Optional[Dict[str, Any]] = {}

class CollectionCreate(CollectionBase):
    pass

class Collection(CollectionBase):
    id: int
    total_books: int
    total_views: int
    total_checkouts: int
    average_rating: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Reading List schemas
class ReadingListBase(BaseModel):
    user_id: int
    name: str
    description: Optional[str] = None
    list_type: str = "custom"
    is_public: bool = False
    is_collaborative: bool = False
    display_order: Optional[List[int]] = []
    target_completion_date: Optional[datetime] = None
    properties: Optional[Dict[str, Any]] = {}

class ReadingListCreate(ReadingListBase):
    pass

class ReadingList(ReadingListBase):
    id: int
    share_code: Optional[str]
    total_books: int
    books_completed: int
    completion_percentage: float
    list_views: int
    books_added_from_list: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Library Event schemas
class LibraryEventBase(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: str
    start_date: datetime
    end_date: Optional[datetime] = None
    duration_hours: Optional[float] = None
    location: Optional[str] = None
    is_virtual: bool = False
    virtual_link: Optional[str] = None
    max_participants: Optional[int] = None
    registration_required: bool = True
    registration_deadline: Optional[datetime] = None
    featured_books: Optional[List[int]] = []
    guest_speakers: Optional[List[Dict[str, str]]] = []
    materials_needed: Optional[List[str]] = []
    age_restrictions: Optional[List[str]] = []
    properties: Optional[Dict[str, Any]] = {}

class LibraryEventCreate(LibraryEventBase):
    pass

class LibraryEvent(LibraryEventBase):
    id: int
    current_registrations: int
    status: str
    actual_attendance: Optional[int]
    satisfaction_rating: Optional[float]
    feedback_summary: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Analytics schemas
class BookAnalytics(BaseModel):
    total_books: int
    total_authors: int
    total_genres: int
    most_popular_books: List[Dict[str, Any]]
    most_popular_authors: List[Dict[str, Any]]
    most_popular_genres: List[Dict[str, Any]]
    recent_additions: List[Dict[str, Any]]
    circulation_stats: Dict[str, int]
    digital_vs_physical: Dict[str, int]
    reading_level_distribution: Dict[str, int]
    condition_distribution: Dict[str, int]

class UserAnalytics(BaseModel):
    total_users: int
    active_users: int
    new_registrations_this_month: int
    membership_distribution: Dict[str, int]
    age_group_distribution: Dict[str, int]
    reading_preferences: Dict[str, int]
    geographic_distribution: Dict[str, int]
    average_books_per_user: float

class CirculationAnalytics(BaseModel):
    total_checkouts: int
    total_returns: int
    active_checkouts: int
    overdue_books: int
    total_reservations: int
    average_checkout_duration: float
    most_borrowed_books: List[Dict[str, Any]]
    checkout_trends: Dict[str, List[Dict[str, Any]]]
    return_rate: float
    renewal_rate: float

class LibraryDashboard(BaseModel):
    book_analytics: BookAnalytics
    user_analytics: UserAnalytics
    circulation_analytics: CirculationAnalytics
    recent_activity: List[Dict[str, Any]]
    upcoming_events: List[Dict[str, Any]]
    system_alerts: List[Dict[str, str]]
    performance_metrics: Dict[str, float]

# Search and Recommendation schemas
class BookSearch(BaseModel):
    query: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    genre: Optional[str] = None
    format_type: Optional[str] = None
    reading_level: Optional[str] = None
    availability_status: Optional[str] = None
    language: Optional[str] = None
    publication_year_from: Optional[int] = None
    publication_year_to: Optional[int] = None
    page_count_min: Optional[int] = None
    page_count_max: Optional[int] = None
    rating_min: Optional[float] = None
    sort_by: Optional[str] = "relevance"  # relevance, title, author, publication_date, rating
    sort_order: Optional[str] = "desc"  # asc, desc
    limit: int = 20
    offset: int = 0

class BookRecommendation(BaseModel):
    user_id: int
    recommendation_type: str  # "similar_books", "trending", "personalized", "genre_based"
    based_on_book_id: Optional[int] = None
    based_on_genre: Optional[str] = None
    limit: int = 10

class RecommendationResult(BaseModel):
    book_id: int
    title: str
    authors: List[str]
    score: float
    reason: str
    similarity_factors: List[str]

# AI Integration schemas
class BookAnalysisRequest(BaseModel):
    book_id: int
    analysis_type: str  # "content_analysis", "sentiment_analysis", "complexity_analysis"
    
class BookAnalysisResult(BaseModel):
    book_id: int
    analysis_type: str
    content_tags: List[str]
    themes: List[str]
    sentiment_score: float
    complexity_score: float
    reading_time_estimate: float
    target_audience: List[str]
    similar_books: List[int]
    
class ReadingInsights(BaseModel):
    user_id: int
    total_books_read: int
    total_pages_read: int
    total_reading_time: float
    average_rating_given: float
    favorite_genres: List[str]
    reading_speed_wpm: float
    reading_consistency: str  # "daily", "weekly", "irregular"
    reading_goals_progress: Dict[str, Any]
    recommendations: List[RecommendationResult]