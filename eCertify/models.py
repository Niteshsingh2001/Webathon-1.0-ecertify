from django.db import models


class Student(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    dob = models.DateField()
    certificate = models.JSONField(default=dict)
