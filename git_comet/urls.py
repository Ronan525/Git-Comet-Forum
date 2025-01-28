"""
URL configuration for git_comet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from forum.views import PostListView  # Import the PostListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Path to allauth app
    path('summernote/', include('django_summernote.urls')),  # Path to django_summernote
    path('forum/', include('forum.urls')),  # Path to forum app
    path('accounts/', include('django.contrib.auth.urls')),  # Path to Django's built-in authentication views
    path('', PostListView.as_view(), name='home'),  # Default path to PostListView
    path('comet/', include('comet.urls')),  # Path to comet app
]