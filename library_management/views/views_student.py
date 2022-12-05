from library_management.models.student import Student
from library_management.serializers import StudentSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


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
def update_student_details(request, id):
    """
    Updates the student with the given id to data given in request body.
    """
    try:
        student = Student.objects.get(pk=id)
    except Student.DoesNotExist:
        return Response({"Message": "Student not found in DB"}, status=status.HTTP_404_NOT_FOUND)
    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
