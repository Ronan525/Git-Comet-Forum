from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import Bio, UserProfile
from django.contrib.auth import update_session_auth_hash


def mybio(request):
    """
    Handle the creation or update of a user's bio.

    If the request method is POST, the function updates the user's bio with the
    provided title and content. Otherwise, it retrieves the user's existing bio
    and renders it on the comet page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered comet page with the user's bio.
    """
    if request.method == 'POST':
        # Retrieve title and content from the POST request
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Get or create a Bio object for the current user
        bio, created = Bio.objects.get_or_create(user=request.user)
        bio.title = title
        bio.content = content
        bio.save()

    # Retrieve the user's bio to display
    bio = Bio.objects.filter(user=request.user).first()
    return render(request, 'comet/comet.html', {'bio': bio})


class UserProfileView(View):
    """
    View to display a user's profile.

    This view retrieves the profile of a user based on their username
    and renders
    it on the comet page.
    """
    template_name = 'comet/comet.html'

    def get(self, request, username):
        """
        Handle GET requests to display a user's profile.

        Args:
            request: The HTTP request object.
            username: The username of the user whose profile is being viewed.

        Returns:
            HttpResponse: The rendered comet page with the user's profile.
        """
        # Retrieve the user object based on the username
        user = get_object_or_404(User, username=username)
        return render(request, self.template_name, {'profile_user': user})


@login_required
def profile(request):
    """
    Handle the display and update of the logged-in user's profile.

    If the request method is POST, the function updates the user's profile
    information, including their password and profile picture. Otherwise, it
    displays the user's current profile information in a form.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered profile page with the user's profile form.
    """
    # Get or create a UserProfile object for the current user
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        # Handle profile update
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            # Save user information
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                # Update the user's password and refresh the session
                user.set_password(password)
                update_session_auth_hash(request, user)
            user.save()

            # Update the user's profile picture
            user_profile.profile_picture = form.cleaned_data.get(
                'profile_picture'
            )
            user_profile.save()

            # Redirect to the profile page after saving
            return redirect('profile')
    else:
        # Display the user's current profile information in a form
        form = UserProfileForm(instance=request.user)

    return render(
        request,
        'comet/profile.html',
        {'form': form, 'user_profile': user_profile}
    )
