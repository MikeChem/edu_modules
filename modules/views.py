# modules/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ModuleListCreateView(APIView):
    def get(self, request):
        return Response({"message": "Список модулей будет здесь"}, status=status.HTTP_200_OK)

    def post(self, request):
        return Response({"message": "Создание модуля"}, status=status.HTTP_201_CREATED)