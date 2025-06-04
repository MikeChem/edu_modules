from django.urls import path, include
from rest_framework.routers import DefaultRouter

from modules.views import (
    CourseViewSet,
    ModuleViewSet,
    LessonViewSet,
    TestViewSet,
    UserProgressViewSet,
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'modules', ModuleViewSet, basename='module')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'tests', TestViewSet, basename='test')
router.register(r'user-progress', UserProgressViewSet, basename='userprogress')

urlpatterns = [
    path('', include(router.urls)),
]