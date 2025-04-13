from django.db import models
from django.conf import settings

# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    # Your Ticket model definition goes here
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/')
    time_created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    # rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        # validators=[MinValueValidator(0), MaxValueValidator(5)])
    # headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    # Your UserFollows model definition goes here
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Following')
    followed_user=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Following_by')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )


class profilemodel(models.Model):
    CHOICE=(('men','Men'),
            ('women','Women'),)
    image=models.ImageField(upload_to='image/')
    description=models.CharField(max_length=100)
    gender=models.CharField(max_length=50,choices=CHOICE)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_profile=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username
