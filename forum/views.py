from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views import View
from django.db import models  # Import models
from .models import Post, ContactMessage, Comment, Rating
from .forms import ContactUsForm, CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

# Create your views here.

class PostListView(generic.ListView):
    model = Post
    template_name = 'forum/index.html'  # Updated template name
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_queryset(self):
        queryset = Post.objects.filter(status=1).order_by('-date_posted')
        for post in queryset:
            post.total_votes = post.ratings.aggregate(total=models.Sum('vote'))['total'] or 0
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['draft_posts'] = Post.objects.filter(author=self.request.user, status=0)
        return context

class ContactUsView(View):
    template_name = 'forum/contact_us.html'

    def get(self, request):
        form = ContactUsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            # Display a success message
            return render(request, self.template_name, {'form': ContactUsForm(), 'success': True})
        return render(request, self.template_name, {'form': form})

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'forum/post_detail.html'
    context_object_name = 'post'

    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.get_object()).order_by('-date_posted')
        context['form'] = CommentForm()
        context['post_form'] = PostForm(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
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
    template_name = 'forum/post_detail.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        comments = Comment.objects.filter(post=post).order_by('-date_posted')
        return render(request, self.template_name, {'post': post, 'comments': comments})

@method_decorator(login_required, name='dispatch')
class PostCreateView(View):
    template_name = 'forum/post_form.html'

    def get(self, request):
        form = PostForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
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
    template_name = 'forum/comment_form.html'

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, author=request.user)
        form = CommentForm(instance=comment)
        return render(request, self.template_name, {'form': form, 'comment': comment})

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, author=request.user)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post-detail', slug=comment.post.slug)
        return render(request, self.template_name, {'form': form, 'comment': comment})

@method_decorator(login_required, name='dispatch')
class CommentDeleteView(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, author=request.user)
        post_slug = comment.post.slug
        comment.delete()
        return redirect('post-detail', slug=post_slug)

@method_decorator(login_required, name='dispatch')
class PostDeleteView(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, author=request.user)
        post.delete()
        return redirect('forum-home')

@method_decorator(login_required, name='dispatch')
class PostPublishView(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, author=request.user)
        post.status = 1  # Set the status to published
        post.save()
        return redirect('post-detail', slug=post.slug)

@login_required
def upvote(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    rating, created = Rating.objects.get_or_create(post=post, user=request.user, defaults={'vote': 1})
    if not created and rating.vote != 1:
        rating.vote = 1
        rating.save(update_fields=['vote'])
    return redirect('forum-home')

@login_required
def downvote(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    rating, created = Rating.objects.get_or_create(post=post, user=request.user, defaults={'vote': -1})
    if not created and rating.vote != -1:
        rating.vote = -1
        rating.save(update_fields=['vote'])
    return redirect('forum-home')