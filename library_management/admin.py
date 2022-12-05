# Register your models here.
from django.contrib import admin
from .models.book import Book
from .models.student import Student
from .models.book_issue import BookIssue

admin.site.register(Book)
admin.site.register(Student)
admin.site.register(BookIssue)
