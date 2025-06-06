# modules/tests/test_api.py

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from modules.models import Course, Module

User = get_user_model()

from rest_framework.test import APIClient


class ModuleAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="apipassword")

        # Используем APIClient и force_authenticate
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # ← вот он ключевой момент!

        # Создаем курс с автором
        self.course = Course.objects.create(
            name="Python", description="Learn Python", author=self.user  # ← также важно!
        )

        # Данные для создания модуля
        self.module_data = {"title": "Django", "description": "Learn Django", "course": self.course.id, "lessons": []}

        self.url = reverse("module-list")

    def test_get_modules(self):
        Module.objects.create(title="Python", description="Learn Python", author=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_module(self):
        print(self.client.get(reverse("module-list")).wsgi_request.user)
        self.module_data["author"] = self.user.id
        response = self.client.post(self.url, self.module_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.count(), 1)
        self.assertEqual(Module.objects.get().title, "Django")
