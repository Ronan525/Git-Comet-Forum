from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment, Rating, ContactMessage
from django.urls import reverse, resolve
from .views import PostListView, PostDetailView
from .forms import CommentForm

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            status=1
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post.')
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertEqual(self.post.status, 1)
        self.assertIsNotNone(self.post.date_posted)

    def test_post_slug_creation(self):
        self.assertEqual(self.post.slug, 'test-post')

    def test_post_str_method(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_excerpt_blank(self):
        self.assertEqual(self.post.excerpt, '')

    def test_post_date_updated(self):
        self.assertIsNotNone(self.post.date_updated)

    def test_post_ordering(self):
        post2 = Post.objects.create(
            title='Another Post',
            content='This is another test post.',
            author=self.user,
            status=1
        )
        posts = Post.objects.all()
        self.assertEqual(posts[0], post2)
        self.assertEqual(posts[1], self.post)

class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            status=1
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment.'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.post.title, 'Test Post')
        self.assertEqual(self.comment.author.username, 'testuser')
        self.assertEqual(self.comment.content, 'This is a test comment.')
        self.assertIsNotNone(self.comment.date_posted)

    def test_comment_str_method(self):
        self.assertEqual(str(self.comment), 'This is a test comment.')

    def test_comment_approved_default(self):
        self.assertFalse(self.comment.approved_comment)

    def test_comment_ordering(self):
        comment2 = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is another test comment.'
        )
        comments = Comment.objects.all()
        self.assertEqual(comments[0], comment2)
        self.assertEqual(comments[1], self.comment)

class RatingModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            status=1
        )
        Rating.objects.filter(post=self.post, user=self.user).delete()
        self.rating = Rating.objects.create(
            post=self.post,
            user=self.user,
            vote=1
        )

    def test_rating_creation(self):
        self.assertEqual(self.rating.post.title, 'Test Post')
        self.assertEqual(self.rating.user.username, 'testuser')
        self.assertEqual(self.rating.vote, 1)

    def test_rating_str_method(self):
        self.assertEqual(str(self.rating), 'testuser - 1')

    def test_rating_total_votes_default(self):
        self.assertEqual(self.rating.total_votes, 0)

    def test_rating_unique_together(self):
        with self.assertRaises(Exception):
            Rating.objects.create(
                post=self.post,
                user=self.user,
                vote=-1
            )

class ContactMessageModelTest(TestCase):

    def setUp(self):
        self.contact_message = ContactMessage.objects.create(
            name='John Doe',
            email='john.doe@example.com',
            message='This is a test message.'
        )

    def test_contact_message_creation(self):
        self.assertEqual(self.contact_message.name, 'John Doe')
        self.assertEqual(self.contact_message.email, 'john.doe@example.com')
        self.assertEqual(self.contact_message.message, 'This is a test message.')
        self.assertIsNotNone(self.contact_message.date_submitted)

    def test_contact_message_str_method(self):
        self.assertEqual(str(self.contact_message), 'Message from John Doe (john.doe@example.com)')

class PostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            status=1
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('forum-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/index.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post_detail.html')

class CommentFormTest(TestCase):
    def test_comment_form_valid(self):
        form_data = {'content': 'This is a test comment.'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        form_data = {'content': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())

class URLTests(TestCase):
    def test_post_list_url_resolves(self):
        url = reverse('forum-home')
        self.assertEqual(resolve(url).func.view_class, PostListView)

    def test_post_detail_url_resolves(self):
        url = reverse('post-detail', args=['test-post'])
        self.assertEqual(resolve(url).func.view_class, PostDetailView)
