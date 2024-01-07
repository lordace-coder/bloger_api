import os
from datetime import timezone
from typing import Any, Dict, Iterable, Optional, Tuple

from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from helpers.format_date import format_time_ago
from notifications_and_messages.models import Notifications

# Create your models here.

User = get_user_model()


class Carousel(models.Model):
    title = models.TextField(max_length=40)
    text = models.TextField(max_length=200)
    image = CloudinaryField()
    link = models.URLField(blank=True, null=True)


class Categories(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Comments(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)

    @property
    def get_formated_date(self):
        return format_time_ago(self.date_created)

    def __str__(self):
        return f"{self.author.username[0:10]} -{self.comment[0:20]}"


class Post(models.Model):
    title = models.TextField(max_length=100)
    post = models.TextField()
    slug = models.SlugField(max_length=100,null=True,blank=True)
    image = CloudinaryField(blank = True,null = True)
    date_created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name="likes",blank=True)
    dislikes = models.ManyToManyField(User,related_name="dislikes",blank=True)
    category = models.ManyToManyField(
        Categories, related_name='categories', blank=True, )

    views = models.IntegerField(default=0)
    comment = models.ManyToManyField(
        Comments, related_name='user_comments', blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    
    
    def verify(self):
        self.verified = True
        self.save()
        
    def view_post(self, user: User):
        qs = ViewPost.objects.filter(post=self, user=user)
        if not qs.exists():
            self.mark_seen()
            new_view = ViewPost.objects.create(post=self, user=user)
            new_view.save()

    def __str__(self):
        return self.title

    def mark_seen(self):
        self.views +=1
        return self.save()
    @property
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    @property
    def get_formated_date(self):
        return format_time_ago(self.date_created)

    def save(self,*args, **kwargs) -> None:
        self.title = self.title.capitalize()
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)




# * LIKE USER POST
    def like_post(self,user:User):
        if self.likes.filter(id = user.id).exists():
            return
        else:
            if self.dislikes.filter(id = user.id).exists():
                self.dislikes.remove(user)
            notification = Notifications.objects.create(user = self.author,notification = f"{self.author.username} liked your post {self.title}")
            notification.save()
            self.likes.add(user)

#  *DISLIKE USER POST
    def dislike_post(self,user:User):
        if self.dislikes.filter(id = user.id).exists():
            return
        else:
            if self.likes.filter(id = user.id).exists():
                self.likes.remove(user)
            notification = Notifications.objects.create(user = self.author,notification = f"{self.author.username} disliked your post {self.title}")
            notification.save()
            self.dislikes.add(user)

class ViewPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def seen(post,user)->bool:
        qs = ViewPost.objects.filter(post=post,user=user).exists()
        return qs