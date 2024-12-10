from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
# Create your models here.

class Habit(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    # created_at= models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name