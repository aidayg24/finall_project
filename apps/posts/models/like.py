from django.contrib.auth.models import User
from django.db import models

from nstagram.apps.posts.models.post import Post


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
