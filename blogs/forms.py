from django import forms
from .models import *

class PostsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    post_id = forms.IntegerField()
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ['content']
    
    def clean_post_id(self):
        post_id = self.cleaned_data.get('post_id')
        
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
             raise forms.ValidationError("The post with the provided ID does not exist.")
        
        return post_id
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content.strip():
            raise forms.ValidationError("Content cannot be empty.")
        return content
    
    def save(self, commit=True):
        post_id = self.cleaned_data.get('post_id')

        post = Post.objects.get(id=post_id)
        comment = super().save(commit=False)
        comment.post = post
        if commit:
            comment.save()
        return comment
