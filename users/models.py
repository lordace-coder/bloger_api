from collections.abc import Iterable

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import Group, User
from django.db import models
from posts.models import Post


# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length = 200,null = True,blank = True)
    mobile = models.CharField(max_length=20,null = True,blank=True)
    image = CloudinaryField(blank = True,null = True)
    full_name = models.CharField(max_length = 200,null = True,blank = True)
    stars = models.ManyToManyField(User,related_name='following',blank=True)


    def get_posts_by_user(self):
        qs = Post.objects.filter(author = self.user).order_by('-date_created')
        if not qs.exists():
            return None
        return qs
    
    @property
    def get_likes_count(self):
        posts = self.get_posts_by_user()
        count = 0
        if posts is not None:
            for i in posts:
                count+= i.likes.count()
        return count

    @property
    def star_count(self)->int:
        return self.stars.count()
    
    @property
    def is_verified(self):
        user = self.user
        verified_group_instance = Group.objects.get(name = 'verified')
        if user.is_authenticated:
            return user.is_staff or user.groups.contains(verified_group_instance)
        return False