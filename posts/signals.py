from django.apps.config import AppConfig
from django.conf import settings
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from notifications_and_messages.models import FlagedUsers, Notifications

from .models import Comments, Post

User = settings.AUTH_USER_MODEL

@receiver(post_save,sender=Post)
def handle_author_notifications(sender,instance:Post,created,*args, **kwargs):
    if created:
        notification = Notifications.objects.create(notification=f"Post {instance.title} created successfully, go view post",user=instance.author)
        notification.save()



@receiver(post_delete,sender = Comments)
def notify_user_comment_deleted(sender,instance:Comments,*args, **kwargs):
    Notifications.objects.create(notification=f"your comment was deleted for violating our policy, contact us if there was a problem",user=instance.author)


@receiver(post_delete,sender = Post)
def notify_user_post_deleted(sender,instance:Post,*args, **kwargs):
    Notifications.objects.create(notification=f"your story was deleted , contact us if there was a problem",user=instance.author)
    
    


# * check if user can save post
@receiver(pre_save,sender=Post)
def verify_user_can_post(sender,instance:Post,*args, **kwargs):
    author = instance.author

    if FlagedUsers.is_flagged(author) and FlagedUsers.objects.get(user=author).is_active:
        Notifications.objects.create(notification=f'your post wasnt uploaded as you are currently flagged',user=author)
        raise Exception('user is banned')
    else:
        return instance
        ...