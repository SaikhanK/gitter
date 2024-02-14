from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth import get_user_model
from django.views import View
from posts.models import Post, Repost
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from itertools import chain
from operator import attrgetter
# Create your views here.
class FollowerPostView(LoginRequiredMixin, CreateView):
    model = CustomUser
    template_name = "user_detail.html"
    fields = ["follower"]
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any):
        following = CustomUser.objects.get(pk = self.kwargs.get("pk"))
        request.user.follower.add(following)
        return super().post(request, *args, **kwargs)
    
    def get_success_url(self) -> str:
        user = self.get_object()
        return reverse("user_detail", kwargs={"pk": user.pk})

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class UserDetailView(DetailView):
    model = CustomUser
    template_name = "user_detail.html"
    context_object_name = "viewed_user"

    def follow(self, request, *args, **kwargs):
        view = FollowerPostView.as_view()
        return view(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_info = CustomUser.objects.filter(following = self.object)
        user_post = Post.objects.filter(author = self.object)
        user_repost = Repost.objects.filter(author = self.object)
        user_content = sorted(chain(user_post, user_repost), key=attrgetter("date"), reverse=True)
        context ["user_info"] = user_info
        context ["user_post"] = user_content
        return context

def followUser(request, pk):
    target_user = get_object_or_404(CustomUser, id = pk)
    current_user = request.user
    if(target_user == current_user):
        print("hat nicht geklappt")
        return render(request, "home.html")
    if current_user.follower.filter(username = target_user).exists():
        print("follower wurde geloescht")
        current_user.follower.remove(target_user)
        return render(request, "home.html")
    current_user.follower.add(target_user)
    print(target_user.pk)
    print(request.user.id)
    return render( request, "home.html")


    
     
    

