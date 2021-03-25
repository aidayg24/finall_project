from django.contrib import admin

from apps.users.models.following import FollowRequest
from apps.users.models.profile import Profile

admin.site.register(Profile)
admin.site.register(FollowRequest)
