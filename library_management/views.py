from datetime import datetime

from .models import Book, Student, BookIssue
from .serializers import BookSerializer, StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

@api_view(['GET'])
def view_all_books(request):
    """
    GET request to view all the books present in the DB currently
    """
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_book(request):
    """
    Takes in a json object to add new book with all the fields of the model book and adds this entry to the DB
    """
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_student(request):
    """
    Takes in a json object to add new student with all the fields of the model student and adds this entry to the DB
    """
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_all_students(request):
    """
     GET request to view all the students present in the DB currently
    """
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def check_out(request):
    """
    POST request with book_id, student_id in request body and if that book's available quantity is more than 0,
    then checks out that book to the given student.
    """
    book_id = request.data['book_id']
    student_id = request.data['student_id']
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({"Message": "Book not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({"Message": "Student not found in DB"}, status=status.HTTP_404_NOT_FOUND)
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
        return Response({"Message": "Book not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({"Message": "Student not found in DB"}, status=status.HTTP_404_NOT_FOUND)

    try:
        book_issued = BookIssue.objects.filter(book_id=book_id, student_id=student_id, status="Borrowed").first()
    except BookIssue.DoesNotExist:
        return Response({"Error": "No books issued currently"}, status=status.HTTP_404_NOT_FOUND)
    book_issue_object = BookIssue.objects.get(id=book_issued.id)
    book_issue_object.status = "Returned"
    book_issue_object.return_date = datetime.today().date()
    book_issue_object.quantity_issued -= 1
    book.quantity_available += 1
    book.save()
    book_issue_object.save()
    return Response({"Message": "Book returned successfully"}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_checkin(request):
    """
    Takes book_id of the book to be returned and book_id of the new book to be issued and the student_id in request
    body and checks in the book returned and checks out the book issued.
    """
    return_book_id = request.data['return_book_id']
    new_book_id = request.data['new_book_id']
    try:
        return_book = Book.objects.get(pk=return_book_id)
    except Book.DoesNotExist:
        return Response({"Message": "Return Book not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    try:
        new_book = Book.objects.get(pk=new_book_id)
    except Book.DoesNotExist:
        return Response({"Message": "New Book not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    student_id = request.data['student_id']
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({"Message": "Student not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    try:
        book_issued = BookIssue.objects.filter(book_id=return_book_id, student_id=student_id, status="Borrowed").first()
    except BookIssue.DoesNotExist:
        return Response({"Error": "No books issued currently"}, status=status.HTTP_404_NOT_FOUND)
    book_issue_object = BookIssue.objects.get(id=book_issued.id)
    book_issue_object.status = "Returned"
    book_issue_object.return_date = datetime.today().date()
    book_issue_object.quantity_issued -= 1
    return_book.quantity_available += 1
    return_book.save()
    book_issue_object.save()
    if new_book.quantity_available >= 1:
        new_book.quantity_available -= 1
        book_issued = BookIssue()
        book_issued.book = new_book
        book_issued.student = student
        book_issued.status = "Borrowed"
        book_issued.quantity_issued += 1
        new_book.save()
        book_issued.save()
    return Response({"Message": "Book returned and issued successfully"}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def get_book_details_by_id(request, id):
    """
    Based on the request type, takes action.
    If it is a GET request, it displays the book with the given id.
    If it is a PUT request, it updates the book with the given id to data given in request body.
    If it is a DELETE request, it deletes the book with the given id.
    """
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return Response({"Message": "Book not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        book.delete()
        return Response({"Message": "Book with given id deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def get_student_details_by_id(request, id):
    """
    Based on the request type, takes action.
    If it is a GET request, it displays the student with the given id.
    If it is a PUT request, it updates the student with the given id to data given in request body.
    If it is a DELETE request, it deletes the student with the given id.
    """
    try:
        student = Student.objects.get(pk=id)
    except Student.DoesNotExist:
        return Response({"Message": "Student not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        return Response({"Message": "Student with given id deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_book(request, id):
    """
    Deletes the book with the given id
    """
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return Response({"Message": "Book not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    book.delete()
    return Response({"Message": "Book deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_student(request, id):
    """
    Deletes the student with the given id
    """
    try:
        student = Student.objects.get(pk=id)
    except Student.DoesNotExist:
        return Response({"Message": "Student not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    student.delete()
    return Response({"Message": "Student deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_book_details(request, id):
    """
    Updates the book with the given id to data given in request body.
    """
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return Response({"Message": "Book not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_student_details(request, id):
    """
    Updates the student with the given id to data given in request body.
    """
    try:
        student = Student.objects.get(pk=id)
    except Book.DoesNotExist:
        return Response({"Message": "Student not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
