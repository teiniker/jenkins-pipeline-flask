import unittest
from book_service_connector import BoookService, Book

class BookServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = BoookService()

    def test_find_by_id(self):
        # Exercise
        book = self.service.find_by_id(1)
        # Verify
        self.assertEqual(1, book.oid)
        self.assertEqual('Eric Matthes', book.author)
        self.assertEqual('978-1718502703', book.isbn)
        self.assertEqual('Python Crash Course', book.title)

    def test_find_all(self):
        # Exercise
        books = self.service.find_all()
        # Verify 
        self.assertEqual(3, len(books))
        self.assertEqual(1, books[0].oid)
        self.assertEqual(2, books[1].oid)
        self.assertEqual(3, books[2].oid)

    def test_insert(self):
        # Exercise
        book = Book(7, "Wes McKinney ", "Python for Data Analysis", "978-1098104030")
        self.service.insert(book)

    def test_update(self):
        # Exercise
        book = Book(2, "Brett Slatkin", "Effective Python", "0134853989")
        self.service.update(book)

if __name__ == '__main__':
    unittest.main()
