# modules/serializers.py

from rest_framework import serializers
from .models import Course, Module, Lesson, Material, Test, Question, AnswerOption, UserProgress


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        for answer in answers_data:
            AnswerOption.objects.create(question=question, **answer)
        return question


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        test = Test.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = Question.objects.create(test=test, **question_data)
            for answer in answers_data:
                AnswerOption.objects.create(question=question, **answer)
        return test


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'title', 'content', 'file']


class LessonSerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True)
    tests = TestSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'materials', 'tests']

    def create(self, validated_data):
        materials_data = validated_data.pop('materials')
        tests_data = validated_data.pop('tests')
        lesson = Lesson.objects.create(**validated_data)
        for material in materials_data:
            Material.objects.create(lesson=lesson, **material)
        for test in tests_data:
            questions_data = test.pop('questions')
            current_test = Test.objects.create(lesson=lesson, **test)
            for question_data in questions_data:
                answers_data = question_data.pop('answers')
                question = Question.objects.create(test=current_test, **question_data)
                for answer in answers_data:
                    AnswerOption.objects.create(question=question, **answer)
        return lesson


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, required=False)  # ← required=False

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'lessons']
        read_only_fields = ['id']

    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons', [])  # ← безопасное извлечение

        module = Module.objects.create(**validated_data)

        for lesson_data in lessons_data:
            materials_data = lesson_data.pop('materials', [])
            tests_data = lesson_data.pop('tests', [])

            lesson = Lesson.objects.create(module=module, **lesson_data)

            for material in materials_data:
                Material.objects.create(lesson=lesson, **material)

            for test_data in tests_data:
                questions_data = test_data.pop('questions', [])
                current_test = Test.objects.create(lesson=lesson, **test_data)

                for question_data in questions_data:
                    answers_data = question_data.pop('answers', [])
                    question = Question.objects.create(test=current_test, **question_data)

                    for answer_data in answers_data:
                        AnswerOption.objects.create(question=question, **answer_data)

        return module


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'modules']

    def create(self, validated_data):
        modules_data = validated_data.pop('modules')
        # Передай author из request
        course = Course.objects.create(author=self.context['request'].user, **validated_data)
        for module_data in modules_data:
            lessons_data = module_data.pop('lessons')
            module = Module.objects.create(course=course, **module_data)
            for lesson_data in lessons_data:
                materials_data = lesson_data.pop('materials')
                tests_data = lesson_data.pop('tests')
                lesson = Lesson.objects.create(module=module, **lesson_data)
                for material in materials_data:
                    Material.objects.create(lesson=lesson, **material)
                for test in tests_data:
                    questions_data = test.pop('questions')
                    current_test = Test.objects.create(lesson=lesson, **test)
                    for question_data in questions_data:
                        answers_data = question_data.pop('answers')
                        question = Question.objects.create(test=current_test, **question_data)
                        for answer in answers_data:
                            AnswerOption.objects.create(question=question, **answer)
        return course


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['id', 'user', 'lesson', 'completed', 'completed_at']