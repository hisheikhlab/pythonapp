from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserTable(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class NewData(models.Model):
    # PRIORITY_CHOICES = [
    #     ('High', 'High'),
    #     ('Medium', 'Medium'),
    #     ('Low', 'Low'),
    # ]
    #
    # priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    priority = models.CharField(max_length=200)
    task = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)  # Add this field for completion status
    due = models.DateField(default="No due date")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task
