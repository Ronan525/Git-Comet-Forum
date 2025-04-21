from django import forms
from allauth.account.forms import LoginForm, SignupForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'form-control custom-input',
            'placeholder': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control custom-input',
            'placeholder': 'Password'
        })
        self.fields['remember'].widget.attrs.update({
            'class': 'form-check-input custom-check'
        })


class CustomSignUpForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control custom-input',
            'placeholder': 'Username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control custom-input',
            'placeholder': 'Email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control custom-input',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control custom-input',
            'placeholder': 'Confirm Password'
        })

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password1', e)
        return password


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']


class UserProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Password'
        }),
        required=False
    )
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
            'username': forms.TextInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Email'
            }),
        }


def test_valid_user_profile_form(self):
    form_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'bio': 'This is a test bio.',
        'profile_picture': '/static/images/default-profile.png',
    }
    form = UserProfileForm(data=form_data)
    self.assertTrue(form.is_valid())
