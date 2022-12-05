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
