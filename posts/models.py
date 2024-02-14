from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.

class Post(models.Model):
    
    title  = models.CharField(max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts_written',
        default=None,
        null=True,
        blank=True,
    )
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.body[:50]
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        default=None,
        null=False,
        blank=False,
    )
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=False,

    )

    def __str__(self):
        return self.body
    
    def get_absolute_url(self):
        return reverse("home")

class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=None
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=None
    )

    def __str__(self):
        return self.author.username
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
class Repost(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=None
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=None
    )

    body = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})