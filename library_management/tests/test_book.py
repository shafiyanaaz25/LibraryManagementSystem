from rest_framework.test import APITestCase
from rest_framework import status

from library_management.helper import create_books


class BookTestCase(APITestCase):

    def test_add_book(self):
        data = {
            "title": "Think and Grow Rich",
            "author": "Napolean Hill",
            "description": "Some people see it as one of the best books of all time to pull you out of depression",
            "quantity_available": 10
        }
        response = self.client.post("/library_management/add_book/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_all_books(self):
        create_books()
        response = self.client.get("/library_management/view_all_books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Think and Grow Rich")

    def test_delete_book(self):
        create_books()
        response = self.client.get("/library_management/view_all_books/")
        self.assertEqual(len(response.data), 2)
        book_id = 1
        response = self.client.delete(f"/library_management/delete_book/{book_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get("/library_management/view_all_books/")
        self.assertEqual(len(response.data), 1)

    def test_update_book_details(self):
        create_books()
        book_id = 1
        response = self.client.get(f"/library_management/book_by_id/{book_id}")
        assert response.data['author'] == "Napolean Hill"
        data = {
            "id": book_id,
            "title": "Think and Grow Rich",
            "author": "abc",
            "description": "Some people see it as one of the best books of all time to pull you out of depression.",
            "quantity_available": 10
        }
        response = self.client.put(f"/library_management/update_book_details/{book_id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"/library_management/book_by_id/{book_id}")
        assert response.data['author'] == "abc"
