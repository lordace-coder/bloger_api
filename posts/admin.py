from django.contrib import admin

from .models import Carousel, Categories, Comments, Post

# Register your models here.

admin.site.register(Carousel)
admin.site.register(Comments)
admin.site.register(Post)
admin.site.register(Categories)
