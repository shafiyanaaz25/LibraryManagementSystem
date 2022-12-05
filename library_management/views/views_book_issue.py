from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from library_management.helper import check_out_book_for_student, check_in_book_for_student
from library_management.models.book import Book
from library_management.models.book_issue import BookIssue
from library_management.models.student import Student


@api_view(['POST'])
def check_out(request):
    """
    POST request with book_id, student_id in request body and if that book's available quantity is more than 0,
    then checks out that book to the given student.
    """
    book_id = request.data['book_id']
    student_id = request.data['student_id']
    response = check_out_book_for_student(book_id, student_id)
    return response


@api_view(['PUT'])
def check_in(request):
    """
    Takes in book_id and student_id in request body to return a book that was already borrowed
    """
    book_id = request.data['book_id']
    student_id = request.data['student_id']
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({"Message": f"Book with id {book_id} not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    try:
        book_issued = BookIssue.objects.filter(book_id=book_id, student_id=student_id, status="Borrowed").first()
    except BookIssue.DoesNotExist:
        return Response({"Error": "No books issued currently"}, status=status.HTTP_404_NOT_FOUND)
    response = check_in_book_for_student(book, book_issued)
    return response


@api_view(['PUT'])
def update_checkin(request):
    """
    Takes book_id of the book to be returned and book_id of the new book to be issued and the student_id in request
    body and checks in the book returned and checks out the book issued.
    """
    return_book_id = request.data['return_book_id']
    try:
        return_book = Book.objects.get(pk=return_book_id)
    except Book.DoesNotExist:
        return Response({"Message": f"Return Book not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    student_id = request.data['student_id']
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({"Message": "Student not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    try:
        book_issued = BookIssue.objects.filter(book_id=return_book_id, student_id=student_id, status="Borrowed").first()
    except BookIssue.DoesNotExist:
        return Response({"Error": "No books issued currently"}, status=status.HTTP_404_NOT_FOUND)
    response = check_in_book_for_student(return_book, book_issued)
    if response.status_code != status.HTTP_200_OK:
        return response

    new_book_id = request.data['new_book_id']
    try:
        new_book = Book.objects.get(pk=new_book_id)
    except Book.DoesNotExist:
        return Response({"Message": f"New Book not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    response = check_out_book_for_student(new_book_id, student_id)
    if response.status_code != status.HTTP_201_CREATED:
        return response
    return Response({"Message": "Book returned and issued successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_books_with_filters(request):
    """
    Takes in student_name, book_name and checkout_date as request body and returns the list of titles of books that
    satisfy the given filters.
    """
    student_name = request.GET.get('student_name')
    book_name = request.GET.get('book_name')
    checkout_date = request.GET.get('checkout_date')
    try:
        book = Book.objects.get(title=book_name)
    except Book.DoesNotExist:
        return Response({"Message": "Book not found in DB with these filters"}, status=status.HTTP_404_NOT_FOUND)
    try:
        student = Student.objects.get(name=student_name)
    except Student.DoesNotExist:
        return Response({"Message": "Student not found in DB with these filters"}, status=status.HTTP_404_NOT_FOUND)
    try:
        books_issued = BookIssue.objects.filter(book_id=book.pk, student_id=student.pk, issue_date=checkout_date)
    except BookIssue.DoesNotExist:
        return Response({"Message": "Book not issued already"}, status=status.HTTP_404_NOT_FOUND)
    books_checked_out = []
    for book_issued in books_issued:
        books_checked_out.append(book_issued.book.title)
    response = {"Books": books_checked_out}
    return Response(response, status=status.HTTP_200_OK)
