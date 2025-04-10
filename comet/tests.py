from django.test import TestCase
from django.contrib.auth.models import User
from .models import Bio, UserProfile
from .forms import ProfilePictureForm, UserProfileForm
from django.urls import reverse, resolve
from .views import update_profile


class BioModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.bio = Bio.objects.create(
            user=self.user,
            title='Test Bio',
            content='This is a test bio.'
        )

    def test_bio_creation(self):
        self.assertEqual(self.bio.user.username, 'testuser')
        self.assertEqual(self.bio.title, 'Test Bio')
        self.assertEqual(self.bio.content, 'This is a test bio.')

    def test_bio_str_method(self):
        self.assertEqual(str(self.bio), 'Test Bio')


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            profile_picture='http://example.com/profile.jpg'
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(
            self.user_profile.profile_picture,
            'http://example.com/profile.jpg'
        )

    def test_user_profile_str_method(self):
        self.assertEqual(str(self.user_profile), 'testuser')


class ProfilePictureFormTest(TestCase):
    def test_valid_profile_picture_form(self):
        form_data = {'profile_picture': 'http://example.com/profile.jpg'}
        form = ProfilePictureForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_profile_picture_form(self):
        form_data = {'profile_picture': ''}
        form = ProfilePictureForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )

    def test_valid_user_profile_form(self):
        form_data = {'bio': 'This is a test bio.'}
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_profile_form(self):
        form_data = {'bio': ''}
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())


class UpdateProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.client.login(username='testuser', password='12345')

    def test_update_profile_view_get(self):
        response = self.client.get(reverse('update-profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comet/update_profile.html')

    def test_update_profile_view_post(self):
        form_data = {'bio': 'Updated bio'}
        response = self.client.post(reverse('update-profile'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.user.refresh_from_db()
        self.assertEqual(self.user.userprofile.bio, 'Updated bio')


class URLTests(TestCase):
    def test_update_profile_url_resolves(self):
        url = reverse('update-profile')
        self.assertEqual(resolve(url).func, update_profile)
