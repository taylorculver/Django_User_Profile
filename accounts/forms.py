from django import forms
from django.contrib.auth.forms import PasswordChangeForm


from . import models


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            'first_name',
            'last_name',
            'email'
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = (
            'DOB',
            'bio',
            'avatar',
        )

