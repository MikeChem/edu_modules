from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# Импорты для OpenAPI / Swagger документации
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    # Админ-панель
    path('admin/', admin.site.urls),

    # API маршруты (через отдельный urls.py в modules)
    path('api/', include('modules.urls')),

    # === Документация через drf-spectacular ===
    # Генерация OpenAPI-схемы
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Интерфейс Swagger UI
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Интерфейс ReDoc
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Подключение MEDIA_URL и MEDIA_ROOT только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
