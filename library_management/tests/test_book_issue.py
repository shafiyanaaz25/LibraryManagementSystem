import datetime
from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework import status

from library_management.helper import create_books, create_students, create_book_issued


class BookStudentTestCase(APITestCase):

    def test_check_out_with_book_id_not_present(self):
        create_books()
        create_students()
        book_id = 4
        student_id = 1
        data = {
            "book_id": book_id,
            "student_id": student_id,
        }
        response = self.client.post(f"/library_management/check_out/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['Message'], "Book not found in DB")

    def test_check_out_with_student_id_not_present(self):
        create_books()
        create_students()
        book_id = 1
        student_id = 5
        data = {
            "book_id": book_id,
            "student_id": student_id,
        }
        response = self.client.post(f"/library_management/check_out/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['Message'], "Student not found in DB")

    def test_check_out(self):
        create_books()
        create_students()
        book_id = 1
        student_id = 1
        data = {
            "book_id": book_id,
            "student_id": student_id,
        }
        response = self.client.post(f"/library_management/check_out/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['Message'], "Book issued successfully")

    def test_check_in(self):
        create_books()
        create_students()
        book_id = 1
        student_id = 1
        data = {
            "book_id": book_id,
            "student_id": student_id,
        }
        response = self.client.post(f"/library_management/check_out/", data)
        response = self.client.put(f"/library_management/check_in/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Message'], "Book returned successfully")

    def test_get_books_by_filter(self):
        create_books()
        create_students()
        create_book_issued()
        book_name = "Think and Grow Rich"
        student_name = "abc"
        checkout_date = datetime.today().date()
        response = self.client.get(
            f"/library_management/filter_books/?book_name={book_name}&student_name={student_name}&checkout_date={checkout_date}")
        self.assertEqual(response.data['Books'], ['Think and Grow Rich'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_check_in(self):
        create_books()
        create_students()
        create_book_issued()
        data = {
            "return_book_id": 1,
            "new_book_id": 2,
            "student_id": 1
        }
        response = self.client.put(f"/library_management/update_check_in/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["Message"], "Book returned and issued successfully")
