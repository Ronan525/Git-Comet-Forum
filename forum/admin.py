from django.contrib import admin
from .models import Post, Comment, Rating, ContactMessage
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'date_posted')
    list_filter = ("status", 'date_posted')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(ContactMessage)