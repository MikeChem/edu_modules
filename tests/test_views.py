# modules/tests/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from modules.models import Module
from rest_framework.test import APIClient  # Импортируем APIClient

User = get_user_model()

class ModuleViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()  # Используем APIClient
        self.client.force_authenticate(user=self.user) # Авторизуем пользователя
        self.module = Module.objects.create(
            title="Python",
            description="Learn Python",
            author=self.user
        )

    def test_module_list_view(self):
        url = reverse('module-list')  # Use the correct name from your urls.py (e.g., 'module-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Проверяем, что ответ содержит ожидаемые данные в формате JSON
        self.assertEqual(len(response.data), 1) # Проверяем, что вернулся один элемент
        self.assertEqual(response.data[0]['title'], 'Python')
        self.assertEqual(response.data[0]['description'], 'Learn Python')

    def test_module_detail_view(self):
        url = reverse('module-detail', args=[self.module.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Python')
        self.assertEqual(response.data['description'], 'Learn Python')