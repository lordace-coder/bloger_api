from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView, RetrieveUpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications_and_messages.models import Notifications
from posts.mixins import StaffEditOnly
from users.models import UserProfile

from .serializers import (UserProfileSearchSerializer, UserProfileSerializer,
                          UserSerializer)


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(['GET'])
def user_info(request):
    if request.user.is_authenticated:
        user = UserSerializer(request.user)
        return Response(user.data)
    else:
        return Response({"error":"user object wasnt found or this user isnt authenticated"},status=404)



class UserProfileApiView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user == obj.user or request.user.is_superuser:
           return super().get(request, *args, **kwargs)
        return Response(status=400,data={"error":"permission denied"})

    def patch(self, request, *args, **kwargs):
        # * manually update email
        email = request.data.get('email')
        if email:
            user = request.user
            user.email = email
            user.save()
        print(request.data.get('image'))
        obj = self.get_object()
        obj.image = request.data.get('image')
        obj.save()
        return super().patch(request, *args, **kwargs)


    def get_object(self):
        queryset = self.get_queryset()
        user =self.request.user
        obj,created = queryset.get_or_create(user = user)
        return obj


class UserProfileVisitorsView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get_object(self):
        author = self.kwargs.get("author")
        qs = self.get_queryset()
        user = User.objects.get(username = author)
        profile,_ = qs.get_or_create(user = user)
        return profile


# class UserSearchView(APIView):
#     serializer_class = UserSerializer

#     def get(self, request):
#         username = request.query_params.get("username")

#         if username is None:
#             raise serializers.ValidationError("Username is required.")

#         users = User.objects.filter(
#             Q(username__icontains=username) | Q(email__icontains=username)
#         )

#         serializer = self.serializer_class(users, many=True)

#         return Response(serializer.data)


class UserSearchView(ListAPIView):
    serializer_class = UserProfileSearchSerializer
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get("username")
        return qs.filter(user__username__icontains = username)




class FollowUserProfile(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):
        requesting_user = request.user
        try:
            user = User.objects.get(username = self.kwargs.get('author'))
            user_profile = UserProfile.objects.get(user = user)
            if user_profile.stars.contains(requesting_user):
                user_profile.stars.remove(requesting_user)
                user_profile.save()
                Notifications.objects.create(
                    notification = f"{requesting_user} just unfollowed you.",
                    user=user,

                )
                return Response('unfollowed succesfully')
            else:
                user_profile.stars.add(requesting_user)
                user_profile.save()
                Notifications.objects.create(
                    notification = f"{requesting_user} started following you",
                    user=user,

                )

                return Response('followed succesfully')
        except Exception as e:
            return Response(f"error occured {e}",status=404)
