# modules/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Course(models.Model):
    name = models.CharField(_('Название курса'), max_length=255)
    description = models.TextField(_('Описание'), blank=True, null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name=_('Автор')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Курс')
        verbose_name_plural = _('Курсы')
        ordering = ['-created_at']


class Module(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,  # ← Позволяем временно пустое значение
        related_name='modules'
    )
    title = models.CharField(_('Заголовок модуля'), max_length=255)
    description = models.TextField(_('Описание'), blank=True, null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name=_('Автор')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Модуль')
        verbose_name_plural = _('Модули')
        ordering = ['-created_at']


class Lesson(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name=_('Модуль')
    )
    title = models.CharField(_('Заголовок урока'), max_length=255)
    content = models.TextField(_('Содержание'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Урок')
        verbose_name_plural = _('Уроки')
        ordering = ['-created_at']


class Material(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name=_('Урок')
    )
    title = models.CharField(_('Заголовок материала'), max_length=255)
    file = models.FileField(_('Файл'), upload_to='lesson_materials/', blank=True, null=True)
    content = models.TextField(_('Текст материала'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Материал')
        verbose_name_plural = _('Материалы')


class Test(models.Model):
    lesson = models.OneToOneField(
        Lesson,
        on_delete=models.CASCADE,
        related_name='test',
        verbose_name=_('Тест для урока')
    )
    title = models.CharField(_('Заголовок теста'), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Тест: {self.lesson.title}'

    class Meta:
        verbose_name = _('Тест')
        verbose_name_plural = _('Тесты')


class Question(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_('Тест')
    )
    text = models.TextField(_('Вопрос'))

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')


class AnswerOption(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name=_('Вопрос')
    )
    text = models.CharField(_('Текст ответа'), max_length=512)
    is_correct = models.BooleanField(_('Правильный?'), default=False)

    def __str__(self):
        return f'{self.text} ({self.is_correct})'

    class Meta:
        verbose_name = _('Вариант ответа')
        verbose_name_plural = _('Варианты ответов')


class UserProgress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='progress',
        verbose_name=_('Пользователь')
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress',
        verbose_name=_('Урок')
    )
    completed = models.BooleanField(_('Завершён'), default=False)
    completed_at = models.DateTimeField(_('Дата завершения'), blank=True, null=True)

    def __str__(self):
        return f'{self.user} — {self.lesson}'

    class Meta:
        verbose_name = _('Прогресс пользователя')
        verbose_name_plural = _('Прогрессы пользователей')
        unique_together = ('user', 'lesson')