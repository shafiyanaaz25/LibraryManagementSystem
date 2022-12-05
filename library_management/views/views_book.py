from rest_framework.decorators import api_view

from library_management.models.book import Book
from library_management.serializers import BookSerializer
from rest_framework.response import Response
from rest_framework import status


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


@api_view(['GET'])
def get_book_details_by_id(request, id):
    """
    It displays the book with the given id.
    """
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return Response({"Message": "Book not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    serializer = BookSerializer(book)
    return Response(serializer.data)


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
