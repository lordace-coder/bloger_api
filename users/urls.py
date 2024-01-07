from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from . import views

urlpatterns = [
    
    path("create_user",views.CreateUserView.as_view()),
    path("get_userdata",views.user_info),
    path("profiles/",views.UserProfileApiView.as_view()),
    path("profiles/<str:author>",views.UserProfileVisitorsView.as_view()),
        path("profiles/<str:author>/follow",views.FollowUserProfile.as_view()),
    path("search-user/",views.UserSearchView.as_view()),
    # simple JWT views
    path('get_token/',TokenObtainPairView.as_view(),name="token_obtain"),
    path('refresh_token/',TokenRefreshView.as_view(),name='refresh_token'),
    path('verify_token/',TokenVerifyView.as_view(),name='verify_token'),

]
