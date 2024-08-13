from django import forms
from .models import *

class PostsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommantsForm(forms.ModelForm):
    class Meta:
        model = Commant
        fields = ['post_id', 'content']