# Generated by Django 4.2.17 on 2025-01-09 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_post_date_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]
