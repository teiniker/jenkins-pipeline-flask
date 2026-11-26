import copy
import unittest
from http import HTTPStatus

from book_service import book_service

# Unit tests for the Commit Stage.
# The Flask test client calls the request handlers directly, without a
# running server and without network communication.

class BookServiceUnitTest(unittest.TestCase):

    def setUp(self):
        # Every test starts with the initial data set
        self.saved_table = copy.deepcopy(book_service.table)
        self.client = book_service.app.test_client()

    def tearDown(self):
        book_service.table[:] = self.saved_table

    def test_find_all(self):
        response = self.client.get('/books')
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(3, len(response.get_json()['data']))

    def test_find_by_id(self):
        response = self.client.get('/books/1')
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('Eric Matthes', response.get_json()['author'])

    def test_find_by_id_not_found(self):
        response = self.client.get('/books/99')
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    def test_insert(self):
        book = {'id': 7, 'author': 'Wes McKinney',
                'title': 'Python for Data Analysis', 'isbn': '978-1098104030'}
        response = self.client.post('/books', json=book)
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertEqual(4, len(book_service.table))

    def test_update(self):
        book = {'author': 'Brett Slatkin', 'title': 'Effective Python',
                'isbn': '0134853989'}
        response = self.client.put('/books/2', json=book)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('0134853989', book_service.table[1]['isbn'])

    # def test_update_not_found(self):
    #     response = self.client.put('/books/99', json={})
    #     self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    def test_delete(self):
        response = self.client.delete('/books/3')
        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)
        self.assertEqual(2, len(book_service.table))

if __name__ == '__main__':
    unittest.main()
