import json
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Book, Student, BookIssue
from .serializers import BookSerializer, BookIssueSerializer, StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

@api_view(['GET', 'POST'])
def view_all_books(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
def get_book_details_by_id(request, id):
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
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
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_all_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def check_out(request):
    book_id = request.data['book_id']
    student_id = request.data['student_id']
    book = Book.objects.get(id=book_id)
    student = Student.objects.get(id=student_id)
    if book.quantity_available >= 1:
        book.quantity_available -= 1
        book_issued = BookIssue()
        book_issued.book = book
        book_issued.student = student
        book_issued.status = "Borrowed"
        book_issued.quantity_issued += 1
        book.save()
        book_issued.save()
        return Response({"message": "Book issued successfully"}, status=status.HTTP_201_CREATED)
    return Response({"error": "quantity not available"})


@api_view(['PUT'])
def check_in(request):
    book_id = request.data['book_id']
    student_id = request.data['student_id']
    book = Book.objects.get(id=book_id)
    if book is None:
        return Response({"Error": "Invalid book id"})
    student = Student.objects.get(id=student_id)
    if student is None:
        return Response({"Error": "Invalid student id"})
    book_issued = BookIssue.objects.filter(book_id=book_id, student_id=student_id, status="Borrowed").first()
    if book_issued is None:
        return Response({"Error": "No books issued currently"})
    book_issue_object = BookIssue.objects.get(id=book_issued.id)
    book_issue_object.status = "Returned"
    book_issue_object.quantity_issued -= 1
    book.quantity_available += 1
    book.save()
    book_issue_object.save()
    return Response({"Message": "Book returned successfully"})


@api_view(['PUT'])
def update_checkin(request):
    return_book_id = request.data['return_book_id']
    new_book_id = request.data['new_book_id']
    student_id = request.data['student_id']
    return_book = Book.objects.get(id=return_book_id)
    new_book = Book.objects.get(id=new_book_id)
    if return_book is None:
        return Response({"Error": "Invalid return book id"})
    student = Student.objects.get(id=student_id)
    if student is None:
        return Response({"Error": "Invalid student id"})
    if new_book is None:
        return Response({"Error": "Invalid issue book id"})
    book_issued = BookIssue.objects.filter(book_id=return_book_id, student_id=student_id, status="Borrowed").first()
    if book_issued is None:
        return Response({"Error": "No books issued currently"})
    book_issue_object = BookIssue.objects.get(id=book_issued.id)
    book_issue_object.status = "Returned"
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
    return Response({"message": "Book returned and issued successfully"}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_book(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_student(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    student.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_book_details(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_student_details(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_books_with_filters(request):
    student_name = request.GET.get('student_name')
    book_name = request.GET.get('book_name')
    checkout_date = request.GET.get('checkout_date')
    book = Book.objects.get(title=book_name)
    student = Student.objects.get(name=student_name)
    books_issued = BookIssue.objects.filter(book_id=book.pk, student_id=student.pk, issue_date=checkout_date)
    books_checked_out = []
    for book_issued in books_issued:
        books_checked_out.append(book_issued.book)
    # serializer = BookSerializer(books, many=True)
    return JsonResponse(json.dumps(books_checked_out), safe=False, status=status.HTTP_200_OK)
    # return Response({"Books": books_checked_out}, status=status.HTTP_200_OK)
