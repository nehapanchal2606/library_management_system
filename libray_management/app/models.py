from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE = [
        ('student', "Student"),
        ('librarian', 'Librarian'),
    ]
    role = models.CharField(max_length=255, choices=ROLE)
    
    def __str__(self):
        return self.username
    
    
class Author(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    bio = models.TextField(default="")
    
    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    
    
class Book(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genres = models.ForeignKey(Genre, on_delete=models.CASCADE)
    ISBN =  models.CharField(max_length=20)
    available_copies =  models.IntegerField()
    total_cpoies =  models.IntegerField()

    
class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned')
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)


class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
