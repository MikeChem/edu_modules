# modules/tests/test_models.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from modules.models import Module, Course


User = get_user_model()

class ModuleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.module = Module.objects.create(
            title="Python",
            description="Learn Python",
            author=self.user
        )

    def test_module_creation(self):
        self.assertTrue(isinstance(self.module, Module))
        self.assertEqual(self.module.title, "Python")
        self.assertEqual(self.module.description, "Learn Python")
        self.assertEqual(self.module.author.username, "testuser")