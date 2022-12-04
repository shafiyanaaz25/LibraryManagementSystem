from datetime import datetime, timedelta

from django.db import models


class Student(models.Model):
    """
    Stores a single student entry
    """
    roll_number = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    department = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    """
    Stores a single book entry
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    quantity_available = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class BookIssue(models.Model):
    """
    Stores a single issued book entry, related to model book and model student
    """
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=25)
    quantity_issued = models.IntegerField(default=0)
    return_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.student} checked out {self.book} on {self.issue_date}"
