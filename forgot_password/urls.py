from django.urls import path

from .views import GenerateTokenApiView

urlpatterns = [
    path('<str:email>',GenerateTokenApiView.as_view(),name='generate-recovery-token'),
]
