import unittest
from book_service_connector import BookService, Book

# Acceptance tests for the user stories in UserStories.md.
# They access the running service only via its REST API (black box tests).
# Every test leaves the data as it was, so the tests don't depend on
# each other or on their order.

class BookServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = BookService()

    def test_find_by_id(self):
        # US-1: Find a book by its ID
        # Exercise
        book = self.service.find_by_id(1)
        # Verify
        self.assertEqual(1, book.oid)
        self.assertEqual('Eric Matthes', book.author)
        self.assertEqual('978-1718502703', book.isbn)
        self.assertEqual('Python Crash Course', book.title)

    def test_find_all(self):
        # US-2: List all books
        # Exercise
        books = self.service.find_all()
        # Verify
        self.assertEqual(3, len(books))
        self.assertEqual(1, books[0].oid)
        self.assertEqual(2, books[1].oid)
        self.assertEqual(3, books[2].oid)

    def test_insert(self):
        # US-3: Add a new book
        # Exercise
        book = Book(7, "Wes McKinney", "Python for Data Analysis", "978-1098104030")
        self.service.insert(book)
        self.addCleanup(self.service.delete, 7)
        # Verify
        stored = self.service.find_by_id(7)
        self.assertEqual("Wes McKinney", stored.author)
        self.assertEqual("Python for Data Analysis", stored.title)
        self.assertEqual("978-1098104030", stored.isbn)

    def test_update(self):
        # US-4: Update an existing book
        # Setup
        original = self.service.find_by_id(2)
        self.addCleanup(self.service.update, original)
        # Exercise
        book = Book(2, "Brett Slatkin", "Effective Python", "0134853989")
        self.service.update(book)
        # Verify
        stored = self.service.find_by_id(2)
        self.assertEqual(2, stored.oid)
        self.assertEqual("0134853989", stored.isbn)

if __name__ == '__main__':
    unittest.main()
