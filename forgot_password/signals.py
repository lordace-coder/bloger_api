from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Token


def generate_mail_template(token):
    mail_template :str= settings.FORGOT_PASSWORD_CONFIG.get('mail_template')
    if mail_template and "#token" in mail_template:
        return mail_template.replace("#token",token)
    else:
        return



@receiver(post_save,sender = Token)
def handle_token_created(sender,instance:Token,created,*args, **kwargs):

    if created:
        if not generate_mail_template(instance.token):
            MAIL_TEMPLATE = f"""
            your verification code is {instance.token},guard it safely.
                """
        else:
            MAIL_TEMPLATE = generate_mail_template(instance.token)
        
        send_mail(
            subject="Recovery Token",
            from_email=settings.EMAIL_HOST_USER,
            message=MAIL_TEMPLATE,
            fail_silently=False,
            recipient_list=[instance.user.email]
        )