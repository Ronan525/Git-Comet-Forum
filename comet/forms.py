from django import forms
from allauth.account.forms import LoginForm, SignupForm
from .models import UserProfile
from django.contrib.auth.models import User

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'form-control custom-input', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control custom-input', 'placeholder': 'Password'})
        self.fields['remember'].widget.attrs.update({'class': 'form-check-input custom-check'})

from allauth.account.forms import SignupForm

class CustomSignUpForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control custom-input', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control custom-input', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control custom-input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control custom-input', 'placeholder': 'Confirm Password'})

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Password'}), required=False)
    profile_picture = forms.ChoiceField(
        choices=[
            ('/static/images/default-profile.png', 'Profile Picture 1'),
            ('/static/images/profile-2.png', 'Profile Picture 2'),
            ('/static/images/profile-3.png', 'Profile Picture 3')
        ],
        widget=forms.Select(attrs={'class': 'form-control custom-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Email'}),
        }