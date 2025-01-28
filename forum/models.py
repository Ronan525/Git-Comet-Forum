from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# This is a tuple of tuples that defines the choices for the status field of the Post model.
STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


# This is the Post model. It has a ForeignKey to the User model, which means that each post is associated with a single user.
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    status = models.IntegerField(choices=STATUS, default=0)
    date_updated = models.DateTimeField(auto_now=True)

# This will order the posts by date_posted in descending order.
    class Meta:
        ordering = ['-date_posted']

# This method will return the title of the post when you call the Post object.
    def __str__(self):
        return self.title
    
# This method will automatically create a slug for the post when you save it.
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # Automatically upvote the post by the author
        Rating.objects.get_or_create(post=self, user=self.author, defaults={'vote': 1})


# This is the Comment model. It has a ForeignKey to the Post model, which means that each comment is associated with a single post.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.content

# This is the Rating model. It has a ForeignKey to the Post model and the User model, which means that each rating is associated with a single post and a single user.
class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    vote = models.IntegerField(choices=[(1, 'Upvote'), (-1, 'Downvote')], null=False)
    total_votes = models.IntegerField(default=0)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.vote}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"