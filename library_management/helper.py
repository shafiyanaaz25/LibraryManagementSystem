from datetime import datetime

from library_management.models.book import Book
from library_management.models.book_issue import BookIssue
from library_management.models.student import Student
from rest_framework.response import Response
from rest_framework import status


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


def check_out_book_for_student(book_id, student_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({"Message": f"Book not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({"Message": f"Student not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    if book.quantity_available >= 1:
        book.quantity_available -= 1
        book_issued = BookIssue()
        book_issued.book = book
        book_issued.student = student
        book_issued.status = "Borrowed"
        book_issued.quantity_issued += 1
        book.save()
        book_issued.save()
        return Response({"Message": "Book issued successfully"}, status=status.HTTP_201_CREATED)
    return Response({"Error": "Quantity not available"}, status=status.HTTP_404_NOT_FOUND)


def check_in_book_for_student(book, book_issued):
    book_issue_object = BookIssue.objects.get(id=book_issued.id)
    book_issue_object.status = "Returned"
    book_issue_object.return_date = datetime.today().date()
    book_issue_object.quantity_issued -= 1
    book.quantity_available += 1
    book.save()
    book_issue_object.save()
    return Response({"Message": "Book returned successfully"}, status=status.HTTP_200_OK)
