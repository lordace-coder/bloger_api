from datetime import datetime, timedelta

from django.conf import settings
from django.db import models

from .generate_token import generate_token

# Create your models here.
user_model = settings.AUTH_USER_MODEL
config :dict |None= settings.FORGOT_PASSWORD_CONFIG
"""
 config = {
     valid_time:timedelta()
     token_length:int(0-10)
     numbers_only:bool
     mail_template = str
 }
"""

class Token(models.Model):
    token = models.CharField(max_length=10,blank = True,null = True)
    user = models.ForeignKey(user_model,on_delete=models.CASCADE)
    expiry = models.DateTimeField(blank = True,null = True)
    created_at = models.DateTimeField(auto_created=True,auto_now=True)


    @staticmethod
    def clear_expired_tokens():
        try:
            current_time = datetime.now()
            qs = Token.objects.all()
            for item in qs:
                if current_time >= item.expiry:
                    item.delete()
        except:
            ...
    
    @staticmethod
    def validate_user_token(user:user_model,token:str)->bool:
        """
        checks if token is valid
        """
        try:
            qs = Token.objects.get(user = user,token = token)
            qs.delete()
            return True
        except:
            return False    

    
    def save(self, *args, **kwargs) -> None:
        # make sure user has an email address
        if not self.user.email:
            raise Exception('Error: users email cannot be null or /',self.user.email,'/')
        # delete past token instances that belong to this user
        
        old_tokens = Token.objects.filter(user = self.user)
        if old_tokens.exists():
            for token_instance in old_tokens:
                token_instance.delete()
                
        if not self.expiry:
            
            self.expiry = datetime.now()+ config.get('valid_time',timedelta(hours=1))
            self.token = generate_token(4)
            
        return super().save(*args, **kwargs)