# modules/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from modules.views import ModuleViewSet, module_list, module_detail

router = DefaultRouter()
router.register(r'api/modules', ModuleViewSet, basename='module')

urlpatterns = [
    path('', module_list, name='module-list'),
    path('<int:pk>/', module_detail, name='module-detail'),
]

urlpatterns += router.urls