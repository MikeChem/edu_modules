from rest_framework import serializers
from modules.models import Module


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']