# Generated by Django 4.2.18 on 2025-01-15 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
