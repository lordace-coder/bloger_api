import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.http import FileResponse, Http404
from django.shortcuts import render
from rest_framework import generics, pagination, status
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications_and_messages.models import (FlagedUsers, Notifications,
                                               Reports)
from users.models import UserProfile

from .mixins import UserEditOnly
from .models import Carousel, Categories, Comments, Post, ViewPost
from .pagination import StandardResultsSetPagination
from .serializers import (CarouselSerializer, CategorySerializer,
                          CommentSerializer, PostCreateSerializer,
                          PostDetailSerializer, PostListSerializers,
                          ReportSerializer)


@api_view(['GET'])
def index(request):
    categories = Categories.objects.all()
    data = CategorySerializer(categories,many = True)
    return Response(data.data)

@api_view(['GET'])
def carousels(request):
    qs = Carousel.objects.all()
    data = CarouselSerializer(qs,many = True)
    return Response(data.data)


class PostsApiView(generics.ListAPIView):
    serializer_class = PostListSerializers
    queryset = Post.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query and not query == ' ':
            look_up = Q(title__icontains = query)|Q(author__username__icontains=query)
            return super().get_queryset().filter(look_up )
        return super().get_queryset().order_by('-date_created').order_by('views').order_by('verified')


class CreatePostView( UserEditOnly,generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()

    def get(self,*args,**kwargs):
        return Response(f"{self.permission_classes}")
    
    def get_profile(self,request):
        query,_ = UserProfile.objects.get_or_create(user = request.user)
        return query
    
    
    def post(self, request, *args, **kwargs):
        category = request.data.get('category')
        user = request.user
        if FlagedUsers.is_flagged(user) and FlagedUsers.objects.get(user=user).is_active:
            
            return Response(status=400,data='user doesnt have posting priviledges')
        # for rest framework view
        if not category:
            category = request.data.get('category.category')
        image = request.data.get('image')
        if not category:
            qs = Categories.objects.get(category="+18")
        else:
            qs = Categories.objects.get(category=category)
        category_data = CategorySerializer(qs,many=False)
        new_dict ={
            'title':request.data.get('title'),
            'post':request.data.get('post'),
            'image':image if image else None,
            'category':category_data.data
        }
        serializer = self.get_serializer(data=new_dict)
        serializer.is_valid(raise_exception=True)

        serializer.save(author = user)
        # * send a notification to your followers that you created a new post
        try:
            qs:UserProfile = self.get_profile(request)
            followers =  qs.stars.all()
            for user in followers:
                # *send notification to each  user following current user
                Notifications.objects.create(notification = f"{request.user} posted a story ... check it out",user = user)
            
        except Exception as e:
            print(f"error occured {e}")
            
        return Response({'success':"post uploaded succesfully"})




class PostDetailApiView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'

  
    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(slug=self.kwargs['slug'])
        user =self.request.user
        is_permitted = (obj.author == self.request.user) or self.request.user.is_superuser

        if user.is_authenticated and not ViewPost.seen(post = obj,user=user):
            obj.view_post(user=user)
        return obj
    
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        obj = queryset.get(slug=self.kwargs['slug'])
        is_permitted = (obj.author == self.request.user) or self.request.user.is_staff
        serializer = self.get_serializer( self.get_object(),context = {'can-update':is_permitted,'request':request})
        return Response(serializer.data,status = 200)





class EditDeletePostView(UserEditOnly,generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    lookup_field = 'slug'

    

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(slug=self.kwargs['slug'])
        return obj

    def patch(self, request, *args, **kwargs):
        user:User = request.user
        obj = Post.objects.get(slug=kwargs.get('slug'))
        if obj.author == user or user.is_superuser:
            category = request.data.get('category')
            qs = Categories.objects.get(category=category)
            image =  request.data.get('image')

            category_data = CategorySerializer(qs,many=False)
            new_dict ={
                'title':request.data.get('title'),
                'post':request.data.get('post'),
                'category':category_data.data
            }
            if image:
                new_dict['image'] = image
            obj = Post.objects.get(slug=kwargs.get('slug'))
            serializer = self.get_serializer(obj,data=new_dict)
            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response({'success':"post uploaded succesfully"},status=200)
        else:
            return Response({"error":"permission denied","suggestions":"use superuser,use owner of post"},status=401)



class CreateComment(UserEditOnly,generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()




    def post(self, request, *args, **kwargs):
        post_slug = kwargs.get('slug')
        data = dict()
        comment = request.POST.get('comment')
        data['comment'] = comment if comment else request.data.get('comment')
        data['author'] = request.user.username
        try:
            post = Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)

        comment = serializer.save(author=request.user)
        post.comment.add(comment)
        post.save()
        Notifications.objects.create(notification=f"{comment.author} commented on your story {post.title}",user=post.author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GetPostBycategory(generics.ListAPIView):
    serializer_class = PostListSerializers
    queryset = Post.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        category = self.kwargs.get('category')
        qs = Categories.objects.filter(category__icontains=category).first()
        new_queryset = self.queryset.filter(category=qs).order_by("?")
        return new_queryset


class TrendingPosts(generics.ListAPIView):
    serializer_class = PostListSerializers
    queryset = Post.objects.order_by('-views')


class LatestPosts(generics.ListAPIView):
    serializer_class = PostListSerializers
    queryset = Post.objects.order_by('-date_created','-views')[0:10]

def get_featured_category(request):
    category = Categories.objects.filter(category__icontains="romance").first()
    return Response(category.category)





class ContactUser(APIView):
    def post(self,request,*args, **kwargs):
        data = request.data
        print(data)
        try:
            send_mail(
                subject=data.get('subject'),
                message=data.get('message'),
                fail_silently=False,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER]
            )
            return Response(status=200)
        except Exception as e:
            return Response(str(e),status=500)
contact_user = ContactUser.as_view()


class PostUserAction(UserEditOnly,APIView):
    queryset = Post.objects.all()

    def get_object(self):
        qs = self.queryset
        return qs.get(slug = self.kwargs.get('slug'))


    def get(self,*args, **kwargs):
        actions = ['like','dislike']
        user_action = kwargs.get('action')

        # check if action is valid
        if user_action in actions:
            obj = self.get_object()
            user:User = self.request.user
            # check if user has liked post before
            if user_action == 'like':
                obj.like_post(user)
                return Response({'data':"post liked"},status = 200)
            else:
                obj.dislike_post(user)
                return Response({'data':"post disliked"},status = 200)
        return Response(status=404)


# todo add to urls
class ReportUser(APIView):
    def get(self,request,*args, **kwargs):
        try:
            msg = request.GET.get('report')
            reported_user = User.objects.get(username = request.GET.get('reported_user'))
            user = request.user
            # * new report 
            Reports.objects.create(reported_user = reported_user,reporting_user = user,report = msg)
            return Response({'data':'succesfull upload'},status=200)
            
        except:
            return Response('report failed,maybe user is invalid',status=400)
        


# * VIEW FOR APP DOWNLOAD
@api_view(['GET'])
def download_app(request):

    apk_file_path = 'files/blorger.apk'  # Replace with the actual path to your APK file
    apk_file = open(apk_file_path, 'rb')
    # apk_file = open('w.txt','w')
    # apk_file.write('dang')
    return FileResponse(apk_file, as_attachment=True)




# *REPORT A USER
class ReportUser(generics.CreateAPIView):
    serializer_class = ReportSerializer
    