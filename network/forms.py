from django import forms
from django.views.generic.edit import FormView
from .models import User, Posts


class post_creation_form(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            "Post_content"
        ]

        labels = {
            "Post_content": ""
        }

        widgets ={
        'Post_content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your post here..'})
        }
