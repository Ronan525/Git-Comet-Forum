from django.urls import path
from .views import mybio, UserProfileView, profile

urlpatterns = [
    path('', mybio, name='mybio'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/', profile, name='profile'),
]