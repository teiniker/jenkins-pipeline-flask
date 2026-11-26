import os
import requests

# The class "BookService" encapsulates the communication with the book
# service REST API.
# With this abstraction we can implement acceptance tests for the book service
# without dealing with the low-level details of HTTP requests and responses.

class Book:
    """Transfer object for Book data"""
    def __init__(self, oid:int, author:str, title:str, isbn:str) -> None:
        self.oid = oid
        self.author = author
        self.title = title
        self.isbn = isbn

class BookService:
    # The URL of the service under test can be set by the pipeline
    BASE_URL = os.environ.get('BOOK_SERVICE_URL', 'http://localhost:9090/books')

    def find_by_id(self, book_id):
        response = requests.get(f'{BookService.BASE_URL}/{book_id}', timeout=5)
        response.raise_for_status()
        data = response.json()
        return Book(
            oid=data['id'],
            author=data['author'],
            title=data['title'],
            isbn=data['isbn'],
        )

    def find_all(self):
        response = requests.get(BookService.BASE_URL, timeout=5)
        response.raise_for_status()
        json_data = response.json()
        return [
            Book(
                oid=book['id'],
                author=book['author'],
                title=book['title'],
                isbn=book['isbn'],
            )
            for book in json_data.get('data', [])
        ]

    def insert(self, book: Book):
        book_data = {
            "id": book.oid,
            "author": book.author,
            "title": book.title,
            "isbn": book.isbn,
        }
        response = requests.post(BookService.BASE_URL, timeout=5, json=book_data)
        response.raise_for_status()

    def update(self, book: Book):
        book_data = {
            "author": book.author,
            "title": book.title,
            "isbn": book.isbn,
        }
        response = requests.put(
            f'{BookService.BASE_URL}/{book.oid}',
            timeout=5,
            json=book_data,
        )
        response.raise_for_status()

    def delete(self, book_id):
        response = requests.delete(f'{BookService.BASE_URL}/{book_id}', timeout=5)
        response.raise_for_status()
