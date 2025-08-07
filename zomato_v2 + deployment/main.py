from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from cachetools import TTLCache
from typing import List
import time

from database import get_db, engine
from models import Book, Base
from schemas import BookCreate, BookUpdate, BookResponse

# Initialize FastAPI app
app = FastAPI(title="Simple Book Store with Caching", version="1.0.0")

# Initialize cache: 100 items max, 5-minute TTL
cache = TTLCache(maxsize=100, ttl=300)

# Create tables on startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("📚 Database tables created!")
    print("🗄️ Cache initialized (100 items, 5-minute TTL)")


# Helper function to generate cache keys
def make_cache_key(operation: str, *args) -> str:
    """Generate a unique cache key"""
    return f"{operation}:{':'.join(map(str, args))}"

# ("get_book",123,241) ---> "getbook:123:241"

# "getbook:123:241" --> Data
# "list_books:0:10" ---> Data
# "list_books:30:40" ---> Data


# Helper function to invalidate related cache entries
def clear_book_cache():
    """Clear all book-related cache entries"""
    keys_to_remove = [key for key in cache.keys() if key.startswith("get_book") or key.startswith("list_books")]
    for key in keys_to_remove:
        cache.pop(key, None)
    print(f"🗑️ Cleared {len(keys_to_remove)} cache entries")


# ============================================================================
# CRUD ENDPOINTS WITH CACHING
# ============================================================================

@app.post("/books/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Create a new book and clear cache"""
    print(f"📝 Creating new book: {book.title}")

    # Create book in database
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    # Clear cache since we added new data
    clear_book_cache()

    return db_book

@app.get("/books/", response_model=List[BookResponse])
def list_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get list of books with caching"""
    cache_key = make_cache_key("list_books", skip, limit)

    # Check cache first
    if cache_key in cache:
        print(f"🟢 CACHE HIT: Returning cached book list (skip={skip}, limit={limit})")
        return cache[cache_key]

    # Cache miss - query database
    print(f"🔴 CACHE MISS: Fetching books from database (skip={skip}, limit={limit})")
    start_time = time.time()

    books = db.query(Book).offset(skip).limit(limit).all()

    query_time = round((time.time() - start_time) * 1000, 2)
    print(f"⏱️ Database query took {query_time}ms")

    # Store in cache
    cache[cache_key] = books
    print(f"💾 Cached {len(books)} books")

    return books





@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get a single book with caching"""
    cache_key = make_cache_key("get_book", book_id)

    # Check cache first
    if cache_key in cache:
        print(f"🟢 CACHE HIT: Returning cached book (ID: {book_id})")
        return cache[cache_key]

    # Cache miss - query database
    print(f"🔴 CACHE MISS: Fetching book {book_id} from database")
    start_time = time.time()

    book = db.query(Book).filter(Book.id == book_id).first()

    query_time = round((time.time() - start_time) * 1000, 2)
    print(f"⏱️ Database query took {query_time}ms")

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Store in cache
    cache[cache_key] = book
    print(f"💾 Cached book: {book.title}")

    return book

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    """Update a book and invalidate cache"""
    print(f"✏️ Updating book {book_id}")

    # Find book
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Update fields
    update_data = book_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)

    # Clear cache since data changed
    clear_book_cache()

    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book and invalidate cache"""
    print(f"🗑️ Deleting book {book_id}")

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    # Clear cache since data changed
    clear_book_cache()

    return {"message": f"Book '{book.title}' deleted successfully"}

# ============================================================================
# CACHE MANAGEMENT ENDPOINTS
# ============================================================================

@app.get("/cache/stats")
def get_cache_stats():
    """Get cache statistics"""
    return {
        "cache_size": len(cache),
        "max_size": cache.maxsize,
        "ttl_seconds": cache.ttl,
        "cache_keys": list(cache.keys())
    }

@app.delete("/cache/clear")
def clear_cache():
    """Manually clear all cache"""
    cache_size = len(cache)
    cache.clear()
    return {"message": f"Cache cleared! Removed {cache_size} entries"}

# ============================================================================
# DEMO & TEST ENDPOINTS
# ============================================================================

@app.get("/demo/cache-test/{book_id}")
def demo_cache_performance(book_id: int, db: Session = Depends(get_db)):
    """Demonstrate cache performance by fetching the same book 3 times"""
    results = []

    for attempt in range(1, 4):
        start_time = time.time()

        try:
            book = get_book(book_id, db)
            response_time = round((time.time() - start_time) * 1000, 2)

            results.append({
                "attempt": attempt,
                "response_time_ms": response_time,
                "book_title": book.title,
                "cache_status": "HIT" if response_time < 10 else "MISS"
            })
        except HTTPException:
            results.append({
                "attempt": attempt,
                "error": "Book not found"
            })
            break

    return {
        "book_id": book_id,
        "performance_test": results,
        "analysis": {
            "first_request": "Database query (slow)",
            "subsequent_requests": "Cache retrieval (fast)"
        }
    }

@app.post("/demo/sample-data")
def create_sample_data(db: Session = Depends(get_db)):
    """Create sample books for testing"""
    sample_books = [
        {"title": "The Python Programming Language", "author": "Guido van Rossum", "price": 45.99, "genre": "Programming"},
        {"title": "FastAPI Modern Python", "author": "Sebastian Ramirez", "price": 39.99, "genre": "Web Development"},
        {"title": "Database Design Patterns", "author": "John Smith", "price": 52.50, "genre": "Database"},
        {"title": "RESTful API Design", "author": "Jane Doe", "price": 29.99, "genre": "API Development"},
        {"title": "Clean Code Principles", "author": "Robert Martin", "price": 42.00, "genre": "Software Engineering"}
    ]

    created_books = []
    for book_data in sample_books:
        # Check if book already exists
        existing = db.query(Book).filter(Book.title == book_data["title"]).first()
        if not existing:
            book = Book(**book_data)
            db.add(book)
            created_books.append(book_data["title"])

    db.commit()
    clear_book_cache()  # Clear cache after adding data

    return {
        "message": f"Created {len(created_books)} sample books",
        "books": created_books
    }

@app.get("/")
def root():
    """API information and instructions"""
    return {
        "message": "📚 Simple Book Store API with Caching",
        "features": [
            "In-memory caching with TTL",
            "Automatic cache invalidation",
            "Performance monitoring",
            "Cache statistics"
        ],
        "quick_start": {
            "1": "POST /demo/sample-data (create sample books)",
            "2": "GET /books/ (list books - cache miss)",
            "3": "GET /books/ (list books - cache hit)",
            "4": "GET /demo/cache-test/1 (see cache performance)",
            "5": "GET /cache/stats (view cache statistics)"
        },
        "endpoints": {
            "books": "/books/",
            "cache_stats": "/cache/stats",
            "performance_demo": "/demo/cache-test/{book_id}"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
