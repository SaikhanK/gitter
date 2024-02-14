from django.urls import path
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/new", PostNewView.as_view(), name="post_new"),
    path("post/<int:pk>/edit", PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name = "post_delete"),
    path("post/<int:pk>/like", likePost, name="post_like"),
    path("post/<int:pk>/repost", RepostView.as_view(), name="post_repost"),
    path("post/<int:pk>/comment", CommentPostView.as_view(), name="post_comment"),
    
]