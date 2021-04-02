from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from apps.posts.models.post import Post


class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='details', on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
    comment = models.TextField('Comment')
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content[:10] + '...'
