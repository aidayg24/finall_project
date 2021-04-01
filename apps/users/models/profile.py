from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from common.validators import check_website


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='media/profile_pics/default.png', upload_to='profile_pics')
    slug = AutoSlugField(populate_from='user')
    followers = models.ManyToManyField("Profile", blank=True)

    first_name = models.CharField('First name', max_length=100, blank=True, null=True)
    last_name = models.CharField('Last name', max_length=100, blank=True, null=True)
    bio = models.CharField('Bio', max_length=255, blank=True, null=True)
    website = models.CharField('Website', blank=True, max_length=150, null=True, validators=[check_website])
    GENDER = [('F', 'female'), ('M', 'male')]
    gender = models.CharField('Gender', max_length=1, choices=GENDER, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return "/users/{}".format(self.slug)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    """
        this function make a profile as soon as we create the user so
        user doesn't have to manually create a profile
    """
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)
