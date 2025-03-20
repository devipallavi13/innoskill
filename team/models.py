from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('on_hold', 'On Hold'),
    )
    username = models.CharField(max_length=150, unique=True)  # Custom username field
    email = models.EmailField(unique=True)  # Explicitly add the email field if needed
    name = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=[('normal', 'Normal'), ('organizer', 'Organizer')])
    organization_verification = models.FileField(upload_to='organization_verification/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.username


class Problem(models.Model):
    STATUS_CHOICES = [
        ('yet_to_start', 'Yet to Start'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
    ]

    problem_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='yet_to_start')

    def __str__(self):
        return self.title
    
class Solution(models.Model):
    solution_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name="solutions")
    organizer = models.ForeignKey('CustomUser', on_delete=models.CASCADE, limit_choices_to={'user_type': 'organizer'})  # Check user_type

    def __str__(self):
        return f"Solution for {self.problem.title} by {self.organizer.username}"
    



