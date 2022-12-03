from django.test import TestCase
import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from library_management.models import Book
from library_management.serializers import BookSerializer


# Create your tests here.

class BookTestCase(APITestCase):
    def test_add_book(self):
        data = {
            "title": "Think and Grow Rich",
            "author": "Napolean Hill",
            "description": "Some people see it as one of the best books of all time to pull you out of depression",
            "quantity_available": 10
        }
        response = self.client.post("/library_management/add_book/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class StudentTestCase(APITestCase):
    def test_add_student(self):
        data = {
            "roll_number": 1,
            "name": "abc",
            "email": "abc@gmail.com",
            "department": "CSE"
        }
        response = self.client.post("/library_management/add_student/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
