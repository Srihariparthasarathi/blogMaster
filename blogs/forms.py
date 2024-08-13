from django import forms
from .models import *

class PostsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    post_id = forms.IntegerField()
    content = forms.CharField(widget=forms.Textarea)

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post_id', 'content']