from django import forms
from .models import Discussion, Post


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ["title"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
