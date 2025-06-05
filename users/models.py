# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Студент"
        TEACHER = "teacher", "Преподаватель"
        ADMIN = "admin", "Администратор"

    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True, null=True)
    bio = models.TextField("О себе", blank=True, null=True)
    role = models.CharField("Роль", max_length=20, choices=Role.choices, default=Role.STUDENT)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
