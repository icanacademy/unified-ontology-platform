#!/usr/bin/env python3

import requests
import json
import time
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8004"

def create_sample_books():
    """Create comprehensive sample book data"""
    books = [
        {
            "title": "The Great Gatsby",
            "subtitle": "A Novel",
            "isbn_10": "0743273565",
            "isbn_13": "9780743273565",
            "publication_date": "1925-04-10T00:00:00",
            "publisher": "Scribner",
            "language": "English",
            "page_count": 180,
            "format_type": "paperback",
            "description": "A classic American novel set in the Jazz Age, exploring themes of wealth, love, idealism, and moral decay",
            "reading_level": "Adult",
            "age_rating": "Teen",
            "condition": "Good",
            "location_code": "FIC-GAT-001",
            "dewey_decimal": "813.52",
            "replacement_cost": 12.99,
            "ebook_available": True,
            "audiobook_available": True,
            "content_tags": ["classic", "american_literature", "jazz_age", "symbolism"],
            "theme_keywords": ["wealth", "love", "american_dream", "moral_decay"]
        },
        {
            "title": "To Kill a Mockingbird",
            "isbn_10": "0061120081",
            "isbn_13": "9780061120084",
            "publication_date": "1960-07-11T00:00:00",
            "publisher": "J.B. Lippincott & Co.",
            "language": "English",
            "page_count": 376,
            "format_type": "hardcover",
            "description": "A gripping tale of racial injustice and childhood innocence set in the American South",
            "reading_level": "Adult",
            "age_rating": "Teen",
            "condition": "Excellent",
            "location_code": "FIC-LEE-001",
            "dewey_decimal": "813.54",
            "replacement_cost": 16.99,
            "ebook_available": True,
            "audiobook_available": True,
            "narrator": "Sissy Spacek",
            "audiobook_duration": 12.5,
            "content_tags": ["classic", "coming_of_age", "social_justice", "southern_gothic"],
            "theme_keywords": ["racism", "justice", "childhood", "moral_courage"]
        },
        {
            "title": "1984",
            "isbn_10": "0451524935",
            "isbn_13": "9780451524935",
            "publication_date": "1949-06-08T00:00:00",
            "publisher": "Signet Classics",
            "language": "English",
            "page_count": 328,
            "format_type": "paperback",
            "description": "A dystopian social science fiction novel about totalitarian surveillance",
            "reading_level": "Adult",
            "age_rating": "Teen",
            "condition": "Good",
            "location_code": "FIC-ORW-001",
            "dewey_decimal": "823.912",
            "replacement_cost": 13.99,
            "ebook_available": True,
            "audiobook_available": True,
            "content_tags": ["dystopian", "science_fiction", "political", "surveillance"],
            "theme_keywords": ["totalitarianism", "surveillance", "freedom", "truth"]
        },
        {
            "title": "Pride and Prejudice",
            "isbn_10": "0141439513",
            "isbn_13": "9780141439518",
            "publication_date": "1813-01-28T00:00:00",
            "publisher": "Penguin Classics",
            "language": "English",
            "page_count": 432,
            "format_type": "paperback",
            "description": "A romantic novel about manners, marriage, and society in Georgian England",
            "reading_level": "Adult",
            "age_rating": "All Ages",
            "condition": "Excellent",
            "location_code": "FIC-AUS-001",
            "dewey_decimal": "823.7",
            "replacement_cost": 14.99,
            "ebook_available": True,
            "audiobook_available": True,
            "content_tags": ["romance", "classic", "regency", "social_commentary"],
            "theme_keywords": ["love", "marriage", "class", "prejudice"]
        },
        {
            "title": "The Catcher in the Rye",
            "isbn_10": "0316769177",
            "isbn_13": "9780316769174",
            "publication_date": "1951-07-16T00:00:00",
            "publisher": "Little, Brown and Company",
            "language": "English",
            "page_count": 277,
            "format_type": "hardcover",
            "description": "A coming-of-age novel about teenage rebellion and alienation",
            "reading_level": "Young Adult",
            "age_rating": "Teen",
            "condition": "Fair",
            "location_code": "FIC-SAL-001",
            "dewey_decimal": "813.54",
            "replacement_cost": 15.99,
            "ebook_available": False,
            "audiobook_available": True,
            "content_tags": ["coming_of_age", "rebellion", "youth", "alienation"],
            "theme_keywords": ["adolescence", "identity", "alienation", "authenticity"]
        },
        {
            "title": "Harry Potter and the Sorcerer's Stone",
            "isbn_10": "0439708184",
            "isbn_13": "9780439708180",
            "publication_date": "1997-06-26T00:00:00",
            "publisher": "Scholastic",
            "language": "English",
            "page_count": 320,
            "format_type": "hardcover",
            "description": "The first book in the beloved fantasy series about a young wizard",
            "reading_level": "Middle Grade",
            "age_rating": "All Ages",
            "condition": "Excellent",
            "location_code": "FAN-ROW-001",
            "dewey_decimal": "823.914",
            "replacement_cost": 17.99,
            "ebook_available": True,
            "audiobook_available": True,
            "narrator": "Jim Dale",
            "audiobook_duration": 8.5,
            "content_tags": ["fantasy", "magic", "adventure", "friendship"],
            "theme_keywords": ["friendship", "courage", "magic", "good_vs_evil"],
            "is_popular_demand": True
        },
        {
            "title": "The Lord of the Rings: The Fellowship of the Ring",
            "isbn_10": "0547928211",
            "isbn_13": "9780547928210",
            "publication_date": "1954-07-29T00:00:00",
            "publisher": "Houghton Mifflin Harcourt",
            "language": "English",
            "page_count": 481,
            "format_type": "paperback",
            "description": "Epic fantasy adventure in Middle-earth",
            "reading_level": "Adult",
            "age_rating": "All Ages",
            "condition": "Good",
            "location_code": "FAN-TOL-001",
            "dewey_decimal": "823.912",
            "replacement_cost": 16.99,
            "ebook_available": True,
            "audiobook_available": True,
            "audiobook_duration": 19.5,
            "content_tags": ["fantasy", "epic", "adventure", "mythology"],
            "theme_keywords": ["heroism", "friendship", "good_vs_evil", "sacrifice"]
        },
        {
            "title": "Introduction to Python Programming",
            "isbn_10": "0134444329",
            "isbn_13": "9780134444321",
            "publication_date": "2019-03-15T00:00:00",
            "publisher": "Pearson",
            "language": "English",
            "page_count": 792,
            "format_type": "paperback",
            "description": "Comprehensive guide to learning Python programming",
            "reading_level": "Adult",
            "age_rating": "All Ages",
            "condition": "Excellent",
            "location_code": "CS-PYT-001",
            "dewey_decimal": "005.133",
            "replacement_cost": 89.99,
            "ebook_available": True,
            "audiobook_available": False,
            "content_tags": ["programming", "python", "computer_science", "tutorial"],
            "theme_keywords": ["programming", "coding", "software_development", "algorithms"]
        }
    ]
    
    print("📚 Creating sample books...")
    created_books = []
    for book in books:
        try:
            response = requests.post(f"{BASE_URL}/books/", json=book)
            if response.status_code == 200:
                book_data = response.json()
                created_books.append(book_data)
                print(f"  ✅ Created: {book['title']}")
            else:
                print(f"  ❌ Failed to create: {book['title']} - {response.text}")
        except Exception as e:
            print(f"  ❌ Error creating {book['title']}: {e}")
    
    return created_books

def create_sample_authors():
    """Create sample authors"""
    authors = [
        {
            "first_name": "F. Scott",
            "last_name": "Fitzgerald",
            "birth_date": "1896-09-24T00:00:00",
            "death_date": "1940-12-21T00:00:00",
            "nationality": "American",
            "biography": "American novelist and short story writer, known for his novels depicting the flamboyance and excess of the Jazz Age."
        },
        {
            "first_name": "Harper",
            "last_name": "Lee",
            "birth_date": "1926-04-28T00:00:00",
            "death_date": "2016-02-19T00:00:00",
            "nationality": "American",
            "biography": "American novelist best known for her 1960 novel To Kill a Mockingbird."
        },
        {
            "first_name": "George",
            "last_name": "Orwell",
            "birth_date": "1903-06-25T00:00:00",
            "death_date": "1950-01-21T00:00:00",
            "nationality": "British",
            "biography": "English novelist, essayist, journalist and critic, best known for 1984 and Animal Farm."
        },
        {
            "first_name": "Jane",
            "last_name": "Austen",
            "birth_date": "1775-12-16T00:00:00",
            "death_date": "1817-07-18T00:00:00",
            "nationality": "British",
            "biography": "English novelist known primarily for her six major novels which interpret the British landed gentry."
        },
        {
            "first_name": "J.K.",
            "last_name": "Rowling",
            "birth_date": "1965-07-31T00:00:00",
            "nationality": "British",
            "biography": "British author, best known for the Harry Potter fantasy series."
        }
    ]
    
    print("👥 Creating sample authors...")
    created_authors = []
    for author in authors:
        try:
            response = requests.post(f"{BASE_URL}/authors/", json=author)
            if response.status_code == 200:
                author_data = response.json()
                created_authors.append(author_data)
                print(f"  ✅ Created: {author['first_name']} {author['last_name']}")
            else:
                print(f"  ❌ Failed to create: {author['first_name']} {author['last_name']}")
        except Exception as e:
            print(f"  ❌ Error creating {author['first_name']} {author['last_name']}: {e}")
    
    return created_authors

def create_sample_users():
    """Create sample library users"""
    users = [
        {
            "user_id": "LIB001",
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice.johnson@email.com",
            "phone": "(555) 123-4567",
            "date_of_birth": "1990-05-15T00:00:00",
            "address": "123 Main St",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62701",
            "membership_type": "standard",
            "preferred_genres": [1, 2, 3],
            "preferred_formats": ["paperback", "ebook"],
            "reading_goals": {"annual_goal": 24, "current_progress": 8}
        },
        {
            "user_id": "LIB002",
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "bob.smith@email.com",
            "phone": "(555) 987-6543",
            "date_of_birth": "1985-12-03T00:00:00",
            "address": "456 Oak Ave",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62702",
            "membership_type": "premium",
            "preferred_genres": [3, 4, 5],
            "preferred_formats": ["hardcover", "audiobook"],
            "reading_goals": {"annual_goal": 36, "current_progress": 15}
        },
        {
            "user_id": "LIB003",
            "first_name": "Carol",
            "last_name": "Davis",
            "email": "carol.davis@email.com",
            "phone": "(555) 456-7890",
            "date_of_birth": "1995-08-20T00:00:00",
            "address": "789 Pine St",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62703",
            "membership_type": "student",
            "preferred_genres": [1, 6, 7],
            "preferred_formats": ["ebook", "paperback"],
            "reading_goals": {"annual_goal": 18, "current_progress": 5}
        }
    ]
    
    print("👤 Creating sample users...")
    created_users = []
    for user in users:
        try:
            response = requests.post(f"{BASE_URL}/users/", json=user)
            if response.status_code == 200:
                user_data = response.json()
                created_users.append(user_data)
                print(f"  ✅ Created: {user['first_name']} {user['last_name']} ({user['user_id']})")
            else:
                print(f"  ❌ Failed to create: {user['first_name']} {user['last_name']}")
        except Exception as e:
            print(f"  ❌ Error creating {user['first_name']} {user['last_name']}: {e}")
    
    return created_users

def create_sample_checkouts(books, users):
    """Create sample checkouts"""
    if not books or not users:
        print("⚠️  No books or users available for creating checkouts")
        return []
    
    print("📖 Creating sample checkouts...")
    created_checkouts = []
    
    # Create some active checkouts
    checkouts = [
        {
            "user_id": users[0]["id"],
            "book_id": books[0]["id"],
            "checkout_method": "in_person"
        },
        {
            "user_id": users[1]["id"],
            "book_id": books[1]["id"],
            "checkout_method": "online"
        },
        {
            "user_id": users[2]["id"],
            "book_id": books[2]["id"],
            "checkout_method": "self_service"
        }
    ]
    
    for checkout in checkouts:
        try:
            response = requests.post(f"{BASE_URL}/checkouts/", json=checkout)
            if response.status_code == 200:
                checkout_data = response.json()
                created_checkouts.append(checkout_data)
                print(f"  ✅ Created checkout: User {checkout['user_id']} -> Book {checkout['book_id']}")
            else:
                print(f"  ❌ Failed to create checkout: {response.text}")
        except Exception as e:
            print(f"  ❌ Error creating checkout: {e}")
    
    return created_checkouts

def create_sample_reviews(books, users):
    """Create sample reviews"""
    if not books or not users:
        print("⚠️  No books or users available for creating reviews")
        return []
    
    print("⭐ Creating sample reviews...")
    reviews = [
        {
            "user_id": users[0]["id"],
            "book_id": books[0]["id"],
            "rating": 5,
            "title": "Absolutely magnificent!",
            "review_text": "A timeless classic that captures the essence of the American Dream. Fitzgerald's prose is beautiful and the story is deeply moving.",
            "reading_date": (datetime.now() - timedelta(days=30)).isoformat()
        },
        {
            "user_id": users[1]["id"],
            "book_id": books[1]["id"],
            "rating": 5,
            "title": "Powerful and important",
            "review_text": "This book changed my perspective on justice and morality. Harper Lee's storytelling is masterful.",
            "reading_date": (datetime.now() - timedelta(days=15)).isoformat()
        },
        {
            "user_id": users[2]["id"],
            "book_id": books[2]["id"],
            "rating": 4,
            "title": "Chilling and relevant",
            "review_text": "Orwell's vision of a dystopian future feels more relevant than ever. A must-read for understanding authoritarianism.",
            "reading_date": (datetime.now() - timedelta(days=7)).isoformat()
        }
    ]
    
    created_reviews = []
    for review in reviews:
        try:
            response = requests.post(f"{BASE_URL}/reviews/", json=review)
            if response.status_code == 200:
                review_data = response.json()
                created_reviews.append(review_data)
                print(f"  ✅ Created review: {review['title']}")
            else:
                print(f"  ❌ Failed to create review: {response.text}")
        except Exception as e:
            print(f"  ❌ Error creating review: {e}")
    
    return created_reviews

def main():
    """Main function to create all sample data"""
    print("🚀 Creating comprehensive sample data for Books & Library Platform")
    print("=" * 70)
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    for i in range(10):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ Server is ready!")
                break
        except:
            time.sleep(2)
    else:
        print("❌ Server not responding. Make sure the backend is running on port 8004")
        return
    
    # Create sample data
    books = create_sample_books()
    time.sleep(1)
    
    authors = create_sample_authors()
    time.sleep(1)
    
    users = create_sample_users()
    time.sleep(1)
    
    checkouts = create_sample_checkouts(books, users)
    time.sleep(1)
    
    reviews = create_sample_reviews(books, users)
    
    print("\n" + "=" * 70)
    print("✅ Sample data creation completed!")
    print(f"📚 Books: {len(books)}")
    print(f"👥 Authors: {len(authors)}")
    print(f"👤 Users: {len(users)}")
    print(f"📖 Checkouts: {len(checkouts)}")
    print(f"⭐ Reviews: {len(reviews)}")
    
    print(f"\n🌐 You can now explore the library at:")
    print(f"  • API Documentation: {BASE_URL}/docs")
    print(f"  • Dashboard Analytics: {BASE_URL}/analytics/dashboard")
    print(f"  • Book Search: {BASE_URL}/books/search")

if __name__ == "__main__":
    main()