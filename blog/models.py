from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Author(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField('title', max_length=200)
    slug = models.SlugField('slug')
    text = models.TextField('text')
    created_date = models.DateTimeField('created_date', auto_now_add=True)
    published_date = models.DateTimeField('published_date', blank=True, null=True)
    updated_date = models.DateTimeField('updated_date', auto_now=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
