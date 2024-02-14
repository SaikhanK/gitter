from django.urls import path
from .views import SignUpView, UserDetailView, FollowerPostView, followUser
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user/<int:pk>/detail", UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/follow",  followUser ,name="user_follow"),
    
]
