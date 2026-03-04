#!/usr/bin/env python3

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uvicorn

# Simple database setup
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./books_simple.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Simple Book model
class SimpleBook(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String)
    isbn = Column(String, unique=True)
    pages = Column(Integer)
    status = Column(String, default="available")
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="Books & Library Management Platform",
    description="Simplified library management system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.get("/")
def root():
    return {
        "message": "Books & Library Management Platform API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/books/")
def list_books(db: Session = Depends(get_db)):
    """Get all books"""
    books = db.query(SimpleBook).all()
    return [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "pages": book.pages,
            "status": book.status
        }
        for book in books
    ]

@app.post("/books/")
def create_book(title: str, author: str = None, isbn: str = None, pages: int = None, db: Session = Depends(get_db)):
    """Create a new book"""
    book = SimpleBook(
        title=title,
        author=author,
        isbn=isbn,
        pages=pages
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "pages": book.pages,
        "status": book.status,
        "message": "Book created successfully"
    }

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get simple statistics"""
    total_books = db.query(SimpleBook).count()
    available_books = db.query(SimpleBook).filter(SimpleBook.status == "available").count()
    
    return {
        "total_books": total_books,
        "available_books": available_books,
        "database_status": "connected"
    }

if __name__ == "__main__":
    print("🚀 Starting Books & Library Management Platform (Simplified)")
    print("📚 Server will be available at: http://localhost:8004")
    print("📖 API Documentation: http://localhost:8004/docs")
    uvicorn.run(app, host="0.0.0.0", port=8004)