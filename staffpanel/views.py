from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications_and_messages.models import (FlagedUsers, Notifications,
                                               Reports, User)
from notifications_and_messages.serializers import NotificationSerializer
from posts.mixins import StaffEditOnly
from posts.models import Post
from posts.serializers import PostDetailSerializer, ReportSerializer


class SendNotification(CreateAPIView):
    """
    send handwriten notifications to users
    """
    serializer_class = NotificationSerializer
    queryset  = Notifications.objects.all()
    
    def perform_create(self, serializer:NotificationSerializer):
        # * uses user id in the user field when sending the post request
        return serializer.save()
        # return super().perform_create(serializer)



class Announcement(StaffEditOnly,APIView):
    """
     Send announcement to all users in thier notifications
    """
    def post(self,request,*args, **kwargs):
        try:
            msg = request.POST.get('message')
            users = User.objects.all()
            for user in users:
                Notifications.objects.create(notification = msg,user=user)
                
            return Response('send succesfully',status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response('internal server error '+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Dashboard(StaffEditOnly,APIView):
    def get(self,request,*args, **kwargs):
        data = {
            'total-users': User.objects.all().count(),
            'posts': Post.objects.all().count(),
            'reports':Reports.objects.all().count(),
        }
        return Response(data)





class UserStatusEdit(APIView):
    def get(self,request,*args, **kwargs):
        data = """
            {
               
                'action_type':options(ban,upgrade,flag)
                'status':options(true,false)
            }
            """
        return Response(data)
    
    def post(self,request,*args, **kwargs):
        requesting_user:User = request.user
        try:
            user = User.objects.get(username = kwargs.get('username'))
            
            #*check action type.. then check if user has permission to perform action
            action_type = request.POST.get('action_type')
            if 'ban' in action_type and requesting_user.is_superuser:
                user.is_active = request.POST.get('status')
                
            elif 'upgrade' in action_type and requesting_user.is_superuser:
                user.is_staff = request.POST.get('status')
            
            elif 'flag' in action_type and requesting_user.is_staff:
                FlagedUsers.flag_user(user=user)
                
            else:
                return Response({'data':'no action was performed,you may not have the required permissions for this task'},status=status.HTTP_401_UNAUTHORIZED)
                
            user.save()
            return Response(status=200)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_509_BANDWIDTH_LIMIT_EXCEEDED)


# * FOR VIEWING REPORTS
class ListReportsApiView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportSerializer