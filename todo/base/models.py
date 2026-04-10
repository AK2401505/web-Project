from django.db import models
from django.contrib.auth.models import AbstractUser

class users(AbstractUser):
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = 'Low', 'Low'
        MEDIUM = 'Medium', 'Medium'
        HIGH = 'High', 'High'
    
    user = models.ForeignKey(users, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=False, blank=False)
    priority = models.CharField(
        max_length=10, 
        choices=Priority.choices, 
        default=Priority.LOW
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    


    