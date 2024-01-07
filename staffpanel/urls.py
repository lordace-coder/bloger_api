from django.urls import path

from . import views

urlpatterns = [
    path('notify',views.SendNotification.as_view()),
    path('announce',views.Announcement.as_view()),
    path('dashboard',views.Dashboard.as_view()),
    path('set-user-status/<str:username>',views.UserStatusEdit.as_view()),
    path('reports/',views.ListReportsApiView.as_view()),
]
