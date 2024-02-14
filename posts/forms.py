from django import forms 

from .models import Comment, Repost

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)

class RepostForm(forms.ModelForm):
    class Meta:
        model = Repost
        fields = ("body",)

