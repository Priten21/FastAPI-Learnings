from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Create the main app object
app = FastAPI()

# Define the structure of our data using Pydantic
# This is like creating a blueprint for our book data.
class Book(BaseModel):
    title: str
    author: str
    pages: int
    genre: Optional[str] = None # This field is optional

# --- API Endpoints ---

# A friendly welcome message at the root URL
@app.get("/")
def say_hello():
    return {"message": "Welcome to your first FastAPI app!"}

# Get a specific book using its ID in the URL path
@app.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    # In a real app, you'd look this up in a database.
    return {"book_id": book_id, "title": "A Sample Book Title"}

# Get a list of all books, with an optional limit
@app.get("/books/")
def get_all_books(limit: int = 10):
    return {"message": f"Showing the first {limit} books."}

# Add a new book by sending data in the request body
@app.post("/books/")
def add_new_book(book: Book):
    return {"status": "success", "message": f"'{book.title}' by {book.author} was added."}

# Update an existing book
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    return {
        "status": "success",
        "message": f"Book ID {book_id} has been updated.",
        "updated_data": book
    }

# --- How to Run This App ---
#
# 1. In your terminal, install the necessary libraries:
#    pip install fastapi "uvicorn[standard]"
#
# 2. Run the server:
#    uvicorn fastapi_basics:app --reload
#
# 3. Open your browser and go to the interactive docs:
#    http://127.0.0.1:8000/docs

