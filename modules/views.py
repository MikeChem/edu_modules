# modules/views.py

from rest_framework import viewsets
from modules.models import Module
from modules.serializers import ModuleSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]  ← можно добавить позже

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

def module_list(request):
    modules = Module.objects.all()
    return render(request, 'module_list.html', {'modules': modules})


def module_detail(request, pk):
    module = Module.objects.get(pk=pk)
    return render(request, 'module_detail.html', {'module': module})