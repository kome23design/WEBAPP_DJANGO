# Generated by Django 5.0 on 2025-04-15 08:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postapp', '0003_alter_comment_body'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='disliked_tickets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_tickets', to=settings.AUTH_USER_MODEL),
        ),
    ]
