from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('download-app',views.download_app),
    path('contact-staff', views.contact_user),
    path('slider', views.carousels),
    path('posts/', views.PostsApiView.as_view()),
    path('post/<slug:slug>', views.PostDetailApiView.as_view(),name="post_detail"),
    path('posts/category/<str:category>',views.GetPostBycategory.as_view()),
    path('trending',views.TrendingPosts.as_view()),
    path('latest',views.LatestPosts.as_view()),
    path('create_post/',views.CreatePostView.as_view()),
    path('edit_post/<slug:slug>',views.EditDeletePostView.as_view()),
    path('comment/<slug:slug>',views.CreateComment.as_view()),
    path('comment/',views.CreateComment.as_view()),
    path('featured-category',views.get_featured_category),
    path('report-user',views.ReportUser.as_view()),

    # * GET USER ACTION likes,dislikes
    path('post/<slug:slug>/action/<str:action>',views.PostUserAction.as_view()),
]


urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
