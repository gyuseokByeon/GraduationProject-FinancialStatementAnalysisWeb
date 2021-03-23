from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from . import managers

class User(AbstractUser):

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"
    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Eail"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    objects = managers.CustomModelManager()

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})