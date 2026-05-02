from django import forms

from .models import Student, Projects, Courses, Subjects


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = "__all__"


class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = "__all__"


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = "__all__"
