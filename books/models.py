from django.db import models
from django.contrib.auth.models import User

from .utils import TrackableModel


class Genre(TrackableModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Publisher(TrackableModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    website = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(TrackableModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.ManyToManyField(Genre)
    amount_of_pages = models.PositiveSmallIntegerField()
    author = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title + ' ' + self.author


class BookComment(TrackableModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()


class BookLike(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
