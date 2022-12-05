from django.db import models


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
