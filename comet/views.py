import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ProfilePictureForm, UserProfileForm
from .models import Bio, UserProfile
from django.contrib.auth import update_session_auth_hash

def mybio(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        bio, created = Bio.objects.get_or_create(user=request.user)
        bio.title = title
        bio.content = content
        bio.save()
    bio = Bio.objects.filter(user=request.user).first()
    return render(request, 'comet/comet.html', {'bio': bio})

class UserProfileView(View):
    template_name = 'comet/comet.html'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        return render(request, self.template_name, {'profile_user': user})

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
                update_session_auth_hash(request, user)
            user.save()
            user_profile.profile_picture = form.cleaned_data.get('profile_picture')
            user_profile.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'comet/profile.html', {'form': form, 'user_profile': user_profile})