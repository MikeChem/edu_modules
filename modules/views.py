from django.shortcuts import render
from rest_framework import viewsets

from modules.models import Course, Module, Lesson, Test, UserProgress
from modules.serializers import CourseSerializer, ModuleSerializer, LessonSerializer, TestSerializer, UserProgressSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# === API ViewSets ===

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer


# === HTML Views (Template-based) ===

# modules/views.py
def module_list(request):
    query = request.GET.get('q')
    modules_list = Module.objects.all()

    if query:
        modules_list = modules_list.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(modules_list, 6)  # 6 модулей на странице
    page = request.GET.get('page')

    try:
        modules = paginator.page(page)
    except PageNotAnInteger:
        modules = paginator.page(1)
    except EmptyPage:
        modules = paginator.page(paginator.num_pages)

    return render(request, 'modules/module_list.html', {'modules': modules})


def module_detail(request, pk):
    module = Module.objects.get(pk=pk)
    return render(request, 'modules/module_detail.html', {'module': module})