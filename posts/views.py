from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import SingleObjectMixin
from .models import Post, Like, Repost
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm, RepostForm
from django.views import View
from accounts.models import CustomUser
from posts.models import Comment, Post 
from django.db.models import Q
from django.http import HttpResponseRedirect

# Create your views here.

class HomePageView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "home.html"


class CommentPostView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "post_detail.html"
    def form_valid(self, form: Any) -> HttpResponse:
        post = get_object_or_404(Post, id = self.kwargs.get("pk"))
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)
    def get_success_url(self):
        post = get_object_or_404(Post, id = self.kwargs.get("pk"))
        return reverse("post_detail", kwargs={"pk": post.pk})


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "post_detail.html"
    form_class = CommentForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        post_comments = Comment.objects.filter(post = self.kwargs.get("pk"))
        context["request_user"] = self.request.user
        context["post_likes"] = Like.objects.filter(post = self.kwargs.get("pk"))
        context["post_comment"] = post_comments
        return context


class PostNewView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_new.html"
    fields = ["title", "body"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ["title", "body"]

    def test_func(self): 
        obj = self.get_object()
        return obj.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")
     
    def test_func(self): 
        obj = self.get_object()
        return obj.author == self.request.user


def likePost(request, pk):
    current_user = request.user
    target_post = get_object_or_404(Post, id = pk)
    if Like.objects.filter(Q(post=target_post) & Q(author=current_user)).exists():
        Like.objects.filter(Q(post=target_post) & Q(author=current_user)).delete()
        return HttpResponseRedirect(reverse("post_detail", kwargs={"pk": target_post.pk}))
    liked_post = Like.objects.create(post=target_post, author=current_user)
    return HttpResponseRedirect(reverse("post_detail", kwargs={"pk": target_post.pk}))


class RepostView(LoginRequiredMixin, CreateView):
    model = Repost
    form_class = RepostForm
    template_name = "post_repost.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form, **kwargs):
        pk = self.kwargs.get("pk")
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk = pk)
        return super().form_valid(form)
    