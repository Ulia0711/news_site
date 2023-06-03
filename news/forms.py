from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import User
from django.db import models


class CustomUserChangeForm(UserChangeForm):
    role = forms.ChoiceField(choices=User.ROLE_TYPES)

    class Meta(UserChangeForm.Meta):
        model = User


class PostForms(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title
