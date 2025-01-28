from django import forms
from .models import Comment, Post

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control custom-input', 'placeholder': 'Write your comment here...'}),
        }

class PostForm(forms.ModelForm):
    draft = forms.BooleanField(required=False, label='Save as Draft')

    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control custom-input', 'placeholder': 'Content'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control custom-input', 'placeholder': 'Excerpt'}),
        }