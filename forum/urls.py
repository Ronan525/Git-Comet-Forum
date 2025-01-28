from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostListView.as_view(), name='forum-home'),
    path('contact/', views.ContactUsView.as_view(), name='contact-us'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('<int:post_id>/upvote/', views.upvote, name='upvote'),
    path('<int:post_id>/downvote/', views.downvote, name='downvote'),
    path('<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('<slug:slug>/publish/', views.PostPublishView.as_view(), name='post-publish'),  # Added publish URL pattern
]