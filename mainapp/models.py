from datetime import datetime
from email.policy import default
from importlib.resources import contents
from pyexpat import model
from turtle import title
from django.db import models
from django.contrib.auth.models import User
import django

# Create your models here.

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField()
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    
class BlogPost(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    datePublished = models.DateTimeField("date published", auto_now_add=True, null = True)
    
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length = 150)
    commenterName = models.TextField(null=True)
    datePublished = models.DateTimeField("date published", auto_now_add=True, null = True)
    
    
