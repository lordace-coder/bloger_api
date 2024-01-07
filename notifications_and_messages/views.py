from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Messages, Notifications, User
from .serializers import MessageSerializer, NotificationSerializer


class NotificationApiView(generics.ListAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationSerializer
    
  
    def get_queryset(self):
        qs = super().get_queryset()           
        user = self.request.user
        return qs.filter(user = user).order_by('-read').order_by('-created_at')

    def get(self, request, *args, **kwargs):
        request_status:str = kwargs.get('status')
        qs = self.get_queryset()
        if request_status and 'delete' in request_status.lower():
            # delete all notifications
            if qs.exists():
                for i in qs:
                    i.delete()
            return Response(status=status.HTTP_200_OK,data = {'data':'deleted all notifications'})
        
        elif request_status and 'read' in request_status:
            # mark all as read
            
            if qs.exists():
                for i in qs:
                    i.mark_as_read()

            return Response(status=status.HTTP_200_OK,data = {'data':'read all notifications'})
        return super().get(request, *args, **kwargs)



# * for messages NOT READY
class MessageApiView(generics.ListCreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        qs = super().get_queryset().filter(Q(author = self.request.user) | Q(reciever =self.request.user))
        return qs
    