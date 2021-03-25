from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from apps.users.models.profile import Profile


class UserRegisterForm(UserCreationForm):
    """
        This is for registration of a new user.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """
        to update the data of user like username and email
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """
            to update the data of profile of user like bio and etc.
        """

    class Meta:
        model = Profile
        fields = ['first_name','last_name', 'gender', 'bio', 'image', 'website']
