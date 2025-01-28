from django.test import TestCase
from django.contrib.auth.models import User
from .models import Bio, UserProfile

class BioModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
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
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            profile_picture='http://example.com/profile.jpg'
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.profile_picture, 'http://example.com/profile.jpg')

    def test_user_profile_str_method(self):
        self.assertEqual(str(self.user_profile), 'testuser')

