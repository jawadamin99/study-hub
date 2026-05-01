from rest_framework.serializers import ModelSerializer

from .models import Projects, Student


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'
