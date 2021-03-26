from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    description = models.CharField('Caption', max_length=255, blank=True)
    pic = models.ImageField('Image', upload_to='path/to/img', blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    user_name = models.ForeignKey('User', User, on_delete=models.CASCADE)
    location = models.CharField('Location', max_length=200, blank=True)
    tags = models.CharField('Tags', max_length=100, blank=True)

    class Meta:
        ordering = ['-date_posted']

    @property
    def time_left_from_post_date(self):
        """
            this function shows how long past
            from the date that the post published
            and we show it like recently or like 2 hours
            ago or 3 month ago and so on
        """
        now = timezone.now()
        duration = now - self.date_posted
        if duration.days == 0 and duration.seconds < 3600:
            return str('recently')

        if duration.days == 0:
            return str(duration.seconds // 3600) + str('  hours ago')

        if duration.days < 32:
            return str(duration.days) + str(' days ago ')

        if duration.days < 365:
            months = duration.days // 30
            if months == 1:
                return str(months) + str(' month ago ')
            else:
                return str(months) + str(' months ago ')

        if duration.days > 365:
            years = (duration.days // 365)
            if years == 1:
                return str(years) + str(' year ago ')
            else:
                return str(years) + str(' years ago ')

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
