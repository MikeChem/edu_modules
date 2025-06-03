# modules/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from modules.models import Module
from modules.serializers import ModuleSerializer

class ModuleListCreateView(APIView):
    def get(self, request):
        return Response({"message": "Список модулей будет здесь"}, status=status.HTTP_200_OK)

    def post(self, request):
        return Response({"message": "Создание модуля"}, status=status.HTTP_201_CREATED)


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)