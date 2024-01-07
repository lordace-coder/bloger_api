from collections.abc import Iterable
from datetime import datetime, timedelta, timezone

from django.contrib.auth.models import User
from django.db import models

from helpers.format_date import format_time_ago


# Create your models here.
class Notifications(models.Model):
    notification = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    
    @property
    def formated_time(self):
        return format_time_ago(self.created_at)

    def mark_as_read(self):
        self.read = True
        self.save()

class Messages(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    reciever = models.ForeignKey(User,on_delete=models.CASCADE,related_name="reciever")
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)





class Reports(models.Model):
    reported_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name= 'reporting')
    reporting_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name= 'reporter')
    report = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    
    def get_previous_reports(self):
        qs = Reports.objects.filter(reported_user = self.reported_user)
        return qs


    def clear_report(self):
        self.delete()




class FlagedUsers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name= 'flagged')
    count = models.IntegerField(default=1)
    date = models.DateTimeField(null = True,blank=True)
    
    @staticmethod
    def is_flagged(user:User):
        qs = FlagedUsers.objects.filter(user = user)
        return qs.exists()
    
    @staticmethod
    def flag_user(user:User):
        # *check if user has been flaged before
        instance,created = FlagedUsers.objects.get_or_create(user = user)
        if created:
            # *notify user that they have been flaged for the first time
            Notifications.objects.create(notification = f'you have been flaged temporarily, during this time you will not be able to perform some actions such as posting or commenting',user=user)
            ...
        else:
            # * notify user that they have been flaged
            instance.count +=1
            instance.save()
            Notifications.objects.create(notification = f'you have been flaged again...anymore and you will get banned,beware',user=user)
        if instance.count >=4:
            user.is_active = False
            user.save()
    
    
    def save(self, *args, **kwargs) -> None:
        self.date = datetime.now()
        return super().save(*args, **kwargs)
    
    
    @property
    def is_active(self):
        # *check if he can now post after being flaged
        current_date = datetime.now(tz=timezone.utc)
        diff :timedelta= current_date - self.date.replace(tzinfo=timezone.utc)

        return diff.days >1

