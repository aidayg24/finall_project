from django.contrib import admin

from apps.posts.models.comment import Comments
from apps.posts.models.like import Like
from apps.posts.models.post import Post

admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Like)
