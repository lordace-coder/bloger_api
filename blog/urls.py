from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('posts.urls')),
    path('admin-tools/',include('staffpanel.urls')),
    path('notifications/',include('notifications_and_messages.urls')),
    path('recovery/',include('forgot_password.urls')),
    path('auth/',include('users.urls')),
    path('admin/', admin.site.urls),
]
