from django.contrib import admin
from .models import Bio
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(Bio)
class BioAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)