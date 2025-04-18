from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views import View
from django.db import models  # Import models
from .models import Post, ContactMessage, Comment, Rating
from .forms import ContactUsForm, CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

# Create your views here.


class PostListView(generic.ListView):

    """
    View to display a list of published posts on the forum.
    Includes pagination and calculates total votes for each post.
    """
    model = Post
    template_name = 'forum/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_queryset(self):
        """
        Fetch only published posts and calculate total votes for each post.
        """
        queryset = Post.objects.filter(status=1).order_by('-date_posted')
        for post in queryset:
            post.total_votes = post.ratings.aggregate(
                total=models.Sum('vote')
            )['total'] or 0
        return queryset

    def get_context_data(self, **kwargs):
        """
        Add draft posts to the context for authenticated users.
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['draft_posts'] = Post.objects.filter(
                author=self.request.user, status=0
            )
        return context


class ContactUsView(View):
    """
    View to handle the Contact Us form submissions.
    Displays the form and processes valid submissions.
    """
    template_name = 'forum/contact_us.html'

    def get(self, request):
        """
        Display the Contact Us form.
        """
        form = ContactUsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Process the submitted Contact Us form.
        Save valid data to the database and display a success message.
        """
        form = ContactUsForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            return render(
                request,
                self.template_name,
                {'form': ContactUsForm(), 'success': True}
            )
        return render(request, self.template_name, {'form': form})


class PostDetailView(generic.DetailView):
    """
    View to display the details of a specific post, including comments.
    Allows users to add comments or update the post if they are the author.
    """
    model = Post
    template_name = 'forum/post_detail.html'
    context_object_name = 'post'

    def get_object(self):
        """
        Fetch the post object based on the slug.
        """
        return get_object_or_404(Post, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        """
        Add comments and forms to the context for the post detail page.
        """
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
            post=self.get_object()
        ).order_by('-date_posted')
        context['form'] = CommentForm()
        context['post_form'] = PostForm(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle form submissions for updating the post or adding a comment.
        """
        post = self.get_object()
        if 'post_id' in request.POST:
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post-detail', slug=post.slug)
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post-detail', slug=post.slug)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


class PostCommentsView(View):
    """
    View to display comments for a specific post.
    """
    template_name = 'forum/post_detail.html'

    def get(self, request, slug):
        """
        Handle GET requests to fetch and display comments for a post.
        """
        post = get_object_or_404(Post, slug=slug)
        comments = Comment.objects.filter(post=post).order_by('-date_posted')
        return render(
            request,
            self.template_name,
            {'post': post, 'comments': comments}
        )


@method_decorator(login_required, name='dispatch')
class PostCreateView(View):
    """
    View to handle the creation of new posts.
    Allows users to save posts as drafts or publish them immediately.
    """
    template_name = 'forum/post_form.html'

    def get(self, request):
        """
        Display the post creation form.
        """
        form = PostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Process the submitted post creation form.
        """
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 0 if form.cleaned_data['draft'] else 1
            post.save()
            return redirect('post-detail', slug=post.slug)
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class CommentUpdateView(View):
    """
    View to handle updating an existing comment.
    """
    template_name = 'forum/comment_form.html'

    def get(self, request, pk):
        """
        Display the comment update form for the logged-in user.
        """
        comment = get_object_or_404(Comment, pk=pk, author=request.user)
        form = CommentForm(instance=comment)
        return render(
            request,
            self.template_name,
            {'form': form, 'comment': comment}
        )

    def post(self, request, pk):
        """
        Process the submitted comment update form.
        """
        comment = get_object_or_404(Comment, pk=pk, author=request.user)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post-detail', slug=comment.post.slug)
        return render(
            request,
            self.template_name,
            {'form': form, 'comment': comment}
        )


@method_decorator(login_required, name='dispatch')
class CommentDeleteView(View):
    """
    View to handle deleting a comment.
    """
    def post(self, request, pk):
        """
        Handle POST requests to delete a comment.
        """
        comment = get_object_or_404(Comment, pk=pk, author=request.user)
        post_slug = comment.post.slug
        comment.delete()
        messages.success(request, "Comment successfully deleted")
        return redirect('post-detail', slug=post_slug)


@method_decorator(login_required, name='dispatch')
class PostDeleteView(View):
    """
    View to handle deleting a post.
    """
    def post(self, request, slug):
        """
        Handle POST requests to delete a post.
        """
        post = get_object_or_404(Post, slug=slug, author=request.user)
        post.delete()
        messages.success(request, "Post successfully deleted")
        return redirect('forum-home')


@method_decorator(login_required, name='dispatch')
class PostPublishView(View):
    """
    View to handle publishing a draft post.
    """
    def post(self, request, slug):
        """
        Handle POST requests to publish a draft post.
        """
        post = get_object_or_404(Post, slug=slug, author=request.user)
        post.status = 1  # Set the status to published
        post.save()
        return redirect('post-detail', slug=post.slug)


@login_required
def upvote(request, post_id):
    """
    Handle upvoting a post by the logged-in user.
    """
    post = get_object_or_404(Post, id=post_id)
    rating, created = Rating.objects.get_or_create(
        post=post, user=request.user, defaults={'vote': 1}
    )
    if not created and rating.vote != 1:
        rating.vote = 1
        rating.save(update_fields=['vote'])
    return redirect('forum-home')


@login_required
def downvote(request, post_id):
    """
    Handle downvoting a post by the logged-in user.
    """
    post = get_object_or_404(Post, id=post_id)
    rating, created = Rating.objects.get_or_create(
        post=post, user=request.user, defaults={'vote': -1}
    )
    if not created and rating.vote != -1:
        rating.vote = -1
        rating.save(update_fields=['vote'])
    return redirect('forum-home')
