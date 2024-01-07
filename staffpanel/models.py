from django.db import models


# Create your models here.
class Actions(models.Model):
    staff = models.CharField(max_length=100)
    action = models.TextField()
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.staff} performed {self.action}"
    
    class Meta:
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'

