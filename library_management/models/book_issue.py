from django.db import models


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
