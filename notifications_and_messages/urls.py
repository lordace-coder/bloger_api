from django.urls import path

from . import views

urlpatterns = [
    path('<str:status>',views.NotificationApiView.as_view()),
    path('',views.NotificationApiView.as_view()),
]
