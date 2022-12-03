from rest_framework import serializers, fields
from .models import Book, BookIssue, Student


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'quantity_available']


class BookIssueSerializer(serializers.ModelSerializer):
    date = fields.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = BookIssue
        fields = ['id', 'student_id', 'book_id', 'issue_date', 'status', 'quantity_issued', 'return_date']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'roll_number', 'name', 'email', 'department']
