from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Float, JSON, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Association Tables for Many-to-Many relationships
book_authors_association = Table(
    'book_authors',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('author_id', Integer, ForeignKey('authors.id'))
)

book_genres_association = Table(
    'book_genres',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

book_collections_association = Table(
    'book_collections',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('collection_id', Integer, ForeignKey('collections.id'))
)

user_favorite_books = Table(
    'user_favorite_books',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('book_id', Integer, ForeignKey('books.id'))
)

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Information
    title = Column(String, nullable=False, index=True)
    subtitle = Column(String)
    isbn_10 = Column(String, unique=True, index=True)
    isbn_13 = Column(String, unique=True, index=True)
    publication_date = Column(DateTime)
    publisher = Column(String)
    edition = Column(String)
    language = Column(String, default="English")
    
    # Physical Properties
    page_count = Column(Integer)
    format_type = Column(String)  # hardcover, paperback, ebook, audiobook
    dimensions = Column(String)  # "6 x 9 x 1 inches"
    weight = Column(Float)  # in grams
    
    # Content Information
    description = Column(Text)
    table_of_contents = Column(Text)
    excerpt = Column(Text)
    age_rating = Column(String)  # "All Ages", "Teen", "Adult"
    reading_level = Column(String)  # "Elementary", "Middle Grade", "Young Adult", "Adult"
    
    # Digital Information
    ebook_available = Column(Boolean, default=False)
    audiobook_available = Column(Boolean, default=False)
    digital_format = Column(JSON)  # PDF, EPUB, MOBI, etc.
    ebook_file_size = Column(Float)  # in MB
    audiobook_duration = Column(Float)  # in hours
    narrator = Column(String)  # for audiobooks
    
    # Acquisition Information
    acquisition_date = Column(DateTime)
    acquisition_method = Column(String)  # purchased, donated, gift, etc.
    acquisition_cost = Column(Float)
    supplier = Column(String)
    
    # Library Management
    location_code = Column(String)  # "A1-B2-C3" shelf location
    barcode = Column(String, unique=True)
    dewey_decimal = Column(String)
    library_of_congress = Column(String)
    condition = Column(String)  # "Excellent", "Good", "Fair", "Poor"
    replacement_cost = Column(Float)
    
    # Status and Availability
    status = Column(String, default="available")  # available, checked_out, reserved, lost, damaged
    is_reference_only = Column(Boolean, default=False)
    is_popular_demand = Column(Boolean, default=False)
    checkout_period_days = Column(Integer, default=14)
    
    # Metrics and Analytics
    total_checkouts = Column(Integer, default=0)
    current_reservations = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    popularity_score = Column(Float, default=0.0)
    
    # AI and Recommendations
    content_tags = Column(JSON)  # AI-generated content tags
    complexity_score = Column(Float)  # reading complexity 1-10
    sentiment_score = Column(Float)  # overall book sentiment
    theme_keywords = Column(JSON)  # extracted themes and topics
    similar_books = Column(JSON)  # IDs of similar books
    
    # Ontology properties
    properties = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    authors = relationship("Author", secondary=book_authors_association, back_populates="books")
    genres = relationship("Genre", secondary=book_genres_association, back_populates="books")
    collections = relationship("Collection", secondary=book_collections_association, back_populates="books")
    checkouts = relationship("Checkout", back_populates="book")
    reservations = relationship("Reservation", back_populates="book")
    reviews = relationship("Review", back_populates="book")
    reading_sessions = relationship("ReadingSession", back_populates="book")

class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal Information
    first_name = Column(String)
    last_name = Column(String, nullable=False)
    middle_name = Column(String)
    pen_names = Column(JSON)  # List of pseudonyms
    birth_date = Column(DateTime)
    death_date = Column(DateTime)
    nationality = Column(String)
    
    # Professional Information
    biography = Column(Text)
    education = Column(JSON)  # List of educational background
    awards = Column(JSON)  # List of awards and honors
    website = Column(String)
    social_media = Column(JSON)  # Social media handles
    
    # Career Metrics
    total_books = Column(Integer, default=0)
    first_publication_date = Column(DateTime)
    latest_publication_date = Column(DateTime)
    most_popular_book_id = Column(Integer, ForeignKey("books.id"))
    
    # Analytics
    average_book_rating = Column(Float, default=0.0)
    total_book_sales = Column(Integer, default=0)
    popularity_trend = Column(String)  # "rising", "stable", "declining"
    
    # Ontology properties
    properties = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    books = relationship("Book", secondary=book_authors_association, back_populates="authors")

class Genre(Base):
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    parent_genre_id = Column(Integer, ForeignKey("genres.id"))  # For hierarchical genres
    
    # Analytics
    total_books = Column(Integer, default=0)
    popularity_score = Column(Float, default=0.0)
    average_rating = Column(Float, default=0.0)
    
    # Ontology properties
    properties = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    books = relationship("Book", secondary=book_genres_association, back_populates="genres")
    parent_genre = relationship("Genre", remote_side=[id])

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Information
    user_id = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    date_of_birth = Column(DateTime)
    
    # Address Information
    address = Column(Text)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String)
    
    # Library Membership
    membership_type = Column(String, default="standard")  # standard, premium, student, faculty
    membership_start_date = Column(DateTime)
    membership_expiry_date = Column(DateTime)
    membership_status = Column(String, default="active")  # active, suspended, expired
    
    # Borrowing Information
    max_concurrent_books = Column(Integer, default=5)
    current_checkouts = Column(Integer, default=0)
    overdue_books = Column(Integer, default=0)
    total_fines = Column(Float, default=0.0)
    
    # Reading Preferences
    preferred_genres = Column(JSON)  # List of preferred genre IDs
    preferred_formats = Column(JSON)  # paperback, hardcover, ebook, audiobook
    reading_goals = Column(JSON)  # Annual reading goals
    reading_challenges = Column(JSON)  # Current reading challenges
    
    # Privacy and Notifications
    privacy_settings = Column(JSON)
    notification_preferences = Column(JSON)
    reading_history_public = Column(Boolean, default=False)
    
    # Analytics and AI
    reading_speed_wpm = Column(Float)  # words per minute
    reading_comprehension_score = Column(Float)
    favorite_topics = Column(JSON)  # AI-analyzed favorite topics
    reading_patterns = Column(JSON)  # Reading time patterns
    personality_profile = Column(JSON)  # Reading personality insights
    
    # Ontology properties
    properties = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    checkouts = relationship("Checkout", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    reading_sessions = relationship("ReadingSession", back_populates="user")
    favorite_books = relationship("Book", secondary=user_favorite_books)
    reading_lists = relationship("ReadingList", back_populates="user")

class Checkout(Base):
    __tablename__ = "checkouts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    
    # Checkout Information
    checkout_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    return_date = Column(DateTime)
    renewal_count = Column(Integer, default=0)
    max_renewals = Column(Integer, default=2)
    
    # Status and Conditions
    checkout_status = Column(String, default="active")  # active, returned, overdue, lost
    checkout_method = Column(String)  # "in_person", "online", "self_service"
    return_method = Column(String)  # "in_person", "drop_box", "self_service"
    return_condition = Column(String)  # "good", "damaged", "lost"
    
    # Fines and Fees
    overdue_fine = Column(Float, default=0.0)
    damage_fee = Column(Float, default=0.0)
    replacement_fee = Column(Float, default=0.0)
    fine_paid = Column(Boolean, default=False)
    
    # Analytics
    actual_reading_time = Column(Float)  # hours spent reading
    completion_percentage = Column(Float)  # how much was read
    user_rating = Column(Float)  # user's rating upon return
    
    # Notes
    checkout_notes = Column(Text)
    return_notes = Column(Text)
    
    # Ontology properties
    properties = Column(JSON)
    
    # Relationships
    user = relationship("User", back_populates="checkouts")
    book = relationship("Book", back_populates="checkouts")

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    
    # Reservation Information
    reservation_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    notification_sent = Column(Boolean, default=False)
    pickup_by_date = Column(DateTime)
    
    # Status
    status = Column(String, default="active")  # active, fulfilled, cancelled, expired
    priority_level = Column(Integer, default=1)  # 1=normal, 2=high, 3=urgent
    
    # Fulfillment
    fulfilled_date = Column(DateTime)
    pickup_date = Column(DateTime)
    
    # Ontology properties
    properties = Column(JSON)
    
    # Relationships
    user = relationship("User", back_populates="reservations")
    book = relationship("Book", back_populates="reservations")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    
    # Review Content
    rating = Column(Integer)  # 1-5 stars
    title = Column(String)
    review_text = Column(Text)
    reading_date = Column(DateTime)
    
    # Review Metadata
    is_verified_reader = Column(Boolean, default=False)  # Actually checked out the book
    helpful_votes = Column(Integer, default=0)
    total_votes = Column(Integer, default=0)
    is_spoiler = Column(Boolean, default=False)
    
    # Content Analysis
    sentiment_score = Column(Float)  # AI-analyzed sentiment
    content_tags = Column(JSON)  # AI-extracted tags
    reading_experience = Column(JSON)  # structured reading experience data
    
    # Moderation
    is_approved = Column(Boolean, default=True)
    moderation_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ontology properties
    properties = Column(JSON)
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")

class ReadingSession(Base):
    __tablename__ = "reading_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    
    # Session Information
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    duration_minutes = Column(Integer)
    
    # Reading Progress
    start_page = Column(Integer)
    end_page = Column(Integer)
    pages_read = Column(Integer)
    completion_percentage = Column(Float)
    
    # Reading Context
    reading_location = Column(String)  # "home", "library", "commute", etc.
    reading_format = Column(String)  # "physical", "ebook", "audiobook"
    device_used = Column(String)  # for digital reading
    
    # Performance Analytics
    reading_speed_wpm = Column(Float)
    comprehension_notes = Column(Text)
    difficulty_rating = Column(Integer)  # 1-5, how difficult was this session
    enjoyment_rating = Column(Integer)  # 1-5, how much did you enjoy it
    
    # Environmental Factors
    interruptions = Column(Integer, default=0)
    environmental_rating = Column(Integer)  # 1-5, reading environment quality
    
    # Ontology properties
    properties = Column(JSON)
    
    # Relationships
    user = relationship("User", back_populates="reading_sessions")
    book = relationship("Book", back_populates="reading_sessions")

class Collection(Base):
    __tablename__ = "collections"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Collection Information
    name = Column(String, nullable=False)
    description = Column(Text)
    collection_type = Column(String)  # "thematic", "curriculum", "seasonal", "featured"
    
    # Organization
    curator_name = Column(String)
    creation_purpose = Column(Text)
    target_audience = Column(JSON)  # age groups, reading levels, interests
    
    # Status and Visibility
    is_public = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    
    # Analytics
    total_books = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    total_checkouts = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ontology properties
    properties = Column(JSON)
    
    # Relationships
    books = relationship("Book", secondary=book_collections_association, back_populates="collections")

class ReadingList(Base):
    __tablename__ = "reading_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # List Information
    name = Column(String, nullable=False)
    description = Column(Text)
    list_type = Column(String)  # "to_read", "currently_reading", "completed", "favorites", "custom"
    
    # Privacy and Sharing
    is_public = Column(Boolean, default=False)
    is_collaborative = Column(Boolean, default=False)
    share_code = Column(String, unique=True)  # for sharing private lists
    
    # Organization
    display_order = Column(JSON)  # ordered list of book IDs
    total_books = Column(Integer, default=0)
    
    # Progress Tracking
    books_completed = Column(Integer, default=0)
    completion_percentage = Column(Float, default=0.0)
    target_completion_date = Column(DateTime)
    
    # Analytics
    list_views = Column(Integer, default=0)
    books_added_from_list = Column(Integer, default=0)  # how many others added books from this list
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ontology properties
    properties = Column(JSON)
    
    # Relationships
    user = relationship("User", back_populates="reading_lists")

class LibraryEvent(Base):
    __tablename__ = "library_events"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Event Information
    title = Column(String, nullable=False)
    description = Column(Text)
    event_type = Column(String)  # "book_club", "author_visit", "workshop", "reading", "discussion"
    
    # Scheduling
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    duration_hours = Column(Float)
    location = Column(String)
    is_virtual = Column(Boolean, default=False)
    virtual_link = Column(String)
    
    # Capacity and Registration
    max_participants = Column(Integer)
    current_registrations = Column(Integer, default=0)
    registration_required = Column(Boolean, default=True)
    registration_deadline = Column(DateTime)
    
    # Event Details
    featured_books = Column(JSON)  # book IDs related to the event
    guest_speakers = Column(JSON)  # speaker information
    materials_needed = Column(JSON)  # what participants should bring
    age_restrictions = Column(JSON)  # age ranges
    
    # Status
    status = Column(String, default="scheduled")  # scheduled, ongoing, completed, cancelled
    
    # Analytics
    actual_attendance = Column(Integer)
    satisfaction_rating = Column(Float)
    feedback_summary = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ontology properties
    properties = Column(JSON)

class LibraryAnalytics(Base):
    __tablename__ = "library_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Time Period
    date = Column(DateTime, default=datetime.utcnow)
    period_type = Column(String)  # "daily", "weekly", "monthly", "yearly"
    
    # Circulation Metrics
    total_checkouts = Column(Integer, default=0)
    total_returns = Column(Integer, default=0)
    new_registrations = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    
    # Collection Metrics
    new_books_added = Column(Integer, default=0)
    books_removed = Column(Integer, default=0)
    most_popular_books = Column(JSON)  # top 10 book IDs
    least_popular_books = Column(JSON)  # bottom 10 book IDs
    
    # Genre Analytics
    popular_genres = Column(JSON)  # genre popularity rankings
    demographic_preferences = Column(JSON)  # age group preferences
    
    # Performance Metrics
    average_checkout_duration = Column(Float)
    overdue_rate = Column(Float)  # percentage of overdue books
    reservation_fulfillment_rate = Column(Float)
    
    # Digital Usage
    ebook_downloads = Column(Integer, default=0)
    audiobook_streams = Column(Integer, default=0)
    digital_vs_physical_ratio = Column(Float)
    
    # Financial Metrics
    revenue_generated = Column(Float, default=0.0)
    operational_costs = Column(Float, default=0.0)
    cost_per_checkout = Column(Float, default=0.0)
    
    # Ontology properties
    properties = Column(JSON)