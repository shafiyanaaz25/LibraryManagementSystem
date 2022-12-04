import datetime
from datetime import datetime
from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from library_management.models import Book, Student, BookIssue


# Create your tests here.
def create_books():
    book_object_1 = Book.objects.create(title="Think and Grow Rich", author="Napolean Hill",
                                        description="Some people see it as one of the best books of all time.",
                                        quantity_available=10)
    book_object_2 = Book.objects.create(title="Think and Grow Rich 1", author="Napolean Hill",
                                        description="Some people see it as one of the best books of all time.",
                                        quantity_available=5)


def create_students():
    student1 = Student.objects.create(roll_number=1, name="abc", email="abc@gmail.com", department="CSE")
    student2 = Student.objects.create(roll_number=2, name="def", email="def@gmail.com", department="Mech")
    student3 = Student.objects.create(roll_number=3, name="xyz", email="xyz@gmail.com", department="Civil")


def create_book_issued():
    book_issued1 = BookIssue.objects.create(book_id=1, student_id=1, issue_date=datetime.today().date(),
                                            status="Borrowed", quantity_issued=1)
    book_issued1 = BookIssue.objects.create(book_id=1, student_id=2, issue_date=datetime.today().date(),
                                            status="Borrowed", quantity_issued=1)
    book_issued3 = BookIssue.objects.create(book_id=2, student_id=3, issue_date=datetime.today().date(),
                                            status="Borrowed", quantity_issued=1)


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


class StudentTestCase(APITestCase):

    def test_add_student(self):
        data = {
            "roll_number": 1,
            "name": "abc",
            "email": "abc@gmail.com",
            "department": "CSE"
        }
        response = self.client.post("/library_management/add_student/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_all_students(self):
        create_students()
        response = self.client.get("/library_management/view_all_students/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["roll_number"], '1')

    def test_delete_student(self):
        create_students()
        response = self.client.get("/library_management/view_all_students/")
        self.assertEqual(len(response.data), 3)
        student_id = 1
        response = self.client.delete(f"/library_management/delete_student/{student_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get("/library_management/view_all_students/")
        self.assertEqual(len(response.data), 2)

    def test_update_student_details(self):
        create_students()
        student_id = 1
        response = self.client.get(f"/library_management/student_by_id/{student_id}")
        # assert response.data['name'] == "abc"
        self.assertEqual(response.data["name"], "abc")
        data = {
            "id": student_id,
            "roll_number": "1",
            "name": "S Naaz",
            "email": "snaaz@gmail.com",
            "department": "CSE"
        }
        response = self.client.put(f"/library_management/update_student_details/{student_id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"/library_management/student_by_id/{student_id}")
        # assert response.data['name'] == "S Naaz"
        self.assertEqual(response.data["name"], "S Naaz")


class BookStudentTestCase(APITestCase):

    def test_check_in_with_book_id_not_present(self):
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

    def test_check_in_with_student_id_not_present(self):
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
