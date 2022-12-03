# Register your models here.
from django.contrib import admin
from .models import Student, Book, BookIssue

admin.site.register(Book)
admin.site.register(Student)
admin.site.register(BookIssue)
