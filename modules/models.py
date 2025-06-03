# modules/models.py

from django.db import models
from users.models import User  # ✅ Теперь всё правильно


class Module(models.Model):
    """
    Модель образовательного модуля.
    """
    title = models.CharField(verbose_name='Название модуля', max_length=255)
    description = models.TextField(verbose_name='Описание модуля', blank=True, null=True)
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Автор модуля',
        related_name='modules'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ['-created_at']