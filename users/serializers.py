from django.contrib.auth.models import Group, User
from rest_framework import serializers

from posts import serializers as post_serializer

from .models import UserProfile
from .validators import validate_email


class UserSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    email = serializers.CharField(validators=[validate_email])
    is_staff =serializers.SerializerMethodField(read_only = True)
    is_admin =serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = User
        fields = ['username','email','password','is_staff',"is_admin","image"]

    def create(self, validated_data:dict):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_is_staff(self,obj:User):
        return obj.is_staff


    def get_is_admin(self,obj):
        return obj.is_superuser

    def get_image(self,obj):
        q,is_created = UserProfile.objects.get_or_create(user=obj)

        image = ''
        if q.image:
            image = q.image.url
            image = str(image).replace('http','https')

        return image


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username',read_only=True)
    email = serializers.CharField(source = 'user.email',read_only=True)
    posts = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    perc_posts = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    is_verified = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    owns_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = (
            "username",
            "full_name",
            "image",
            "mobile",
            "address",
            "posts",
            "owns_profile",
            "email",
            "post_count",
            "perc_posts",
            'star_count',
            'is_verified',
            'following',
            'likes',
        )
        
        
    def get_likes(self,obj):
        return obj.get_likes_count

    def get_owns_profile(self,obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.username == obj.user.username
        return False
    def get_image(self,obj):
        image = None
        if obj.image:
            image = obj.image.url
            image = str(image).replace('http','https')

        return image
    def get_post_count(self,obj):
        count = 0
        posts = obj.get_posts_by_user()
        if not posts:
            return count
        count= posts.count()
        return count

    def get_perc_posts(self,obj):
        count = 0
        posts = obj.get_posts_by_user()
        if not posts:
            return count
        count= posts.count()
        perc = (count/150) *100
        return perc
    def get_posts(self,obj):
        posts = obj.get_posts_by_user()
        q = None
        if posts:
            return post_serializer.PostListSerializers(posts,many=True,context=self.context).data


    def get_is_verified(self,obj):
        return obj.is_verified
    
    def get_following(self,obj:UserProfile):
        requesting_user = self.context.get('request').user
        if requesting_user.is_authenticated:
            return obj.stars.contains(requesting_user)
        return False


class UserProfileSearchSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username',read_only=True)
    email = serializers.CharField(source = 'user.email',read_only=True)
    image = serializers.SerializerMethodField()
    is_verified = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    owns_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = (
            "username",
            "full_name",
            "image",
            "mobile",
            "address",
            "email",
            'star_count',
            'is_verified',
            'following',
            'owns_profile',
        )
        
    def get_owns_profile(self,obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.username == obj.user.username
        return False

    
    def get_image(self,obj):
        image = None
        if obj.image:
            image = obj.image.url
            image = str(image).replace('http','https')

        return image
 

    def get_is_verified(self,obj):
        user = obj.user
        verified_group_instance = Group.objects.get(name = 'verified')
        if user.is_authenticated:
            return user.is_staff or user.groups.contains(verified_group_instance)
    
    def get_following(self,obj:UserProfile):
        requesting_user = self.context.get('request').user
        if requesting_user.is_authenticated:
            return obj.stars.contains(requesting_user)
        return False

