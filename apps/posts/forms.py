from django import forms

from apps.posts.models.comment import Comments
from apps.posts.models.post import Post


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'pic', 'location', 'tags']


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
