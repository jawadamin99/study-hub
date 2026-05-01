from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .forms import StudentForm, ProjectForm, CourseForm, SubjectForm
from .models import Student, Projects, Courses, Subjects
from .serializers import StudentSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['first_name', 'email']
    search_fields = ['first_name', 'email']
    ordering_fields = ['id', 'first_name', 'email']
    ordering = ['id']


@login_required
def student_list(request):
    students = Student.objects.all()
    search = request.GET.get('search')
    if search:
        students = students.filter(first_name__icontains=search)
    age = request.GET.get('age')

    if age:
        students = students.filter(age=age)
    return render(request, 'students/list.html', {'students': students})


@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/form.html', {'form': form})


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, id=pk)
    if request.method == 'POST':
        if student:
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                return redirect('student_list')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/form.html', {'form': form})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()
    return redirect('student_list')


@login_required
def project_list(request):
    projects = Projects.objects.select_related("owner").all()
    rows = [
        {
            "cells": [
                project.name,
                project.description,
                project.owner.email if project.owner else "Unassigned",
                "Active" if project.is_active else "Inactive",
            ],
            "edit_url": "project_update",
            "delete_url": "project_delete",
            "pk": project.pk,
        }
        for project in projects
    ]
    context = {
        "page_title": "Projects",
        "eyebrow": "Project Space",
        "heading": "Projects",
        "description": "Track projects, their owners, and whether they are currently active.",
        "columns": ["Name", "Description", "Owner", "Status"],
        "rows": rows,
        "create_url": "project_create",
        "create_label": "Create Project",
    }
    return render(request, "resources/list.html", context)


@login_required
def course_list(request):
    courses = Courses.objects.all()
    rows = [
        {
            "cells": [course.title, course.description],
            "edit_url": "course_update",
            "delete_url": "course_delete",
            "pk": course.pk,
        }
        for course in courses
    ]
    context = {
        "page_title": "Courses",
        "eyebrow": "Course Catalog",
        "heading": "Courses",
        "description": "Browse the available courses and their descriptions in one place.",
        "columns": ["Title", "Description"],
        "rows": rows,
        "create_url": "course_create",
        "create_label": "Create Course",
    }
    return render(request, "resources/list.html", context)


@login_required
def subject_list(request):
    subjects = Subjects.objects.all()
    rows = [
        {
            "cells": [subject.title],
            "edit_url": "subject_update",
            "delete_url": "subject_delete",
            "pk": subject.pk,
        }
        for subject in subjects
    ]
    context = {
        "page_title": "Subjects",
        "eyebrow": "Subject Library",
        "heading": "Subjects",
        "description": "See the configured subject list used across students, teachers, and courses.",
        "columns": ["Title"],
        "rows": rows,
        "create_url": "subject_create",
        "create_label": "Create Subject",
    }
    return render(request, "resources/list.html", context)


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("project_list")
    else:
        form = ProjectForm()

    context = {
        "page_title": "Create Project",
        "eyebrow": "Project Space",
        "heading": "Create Project",
        "description": "Add a new project and optionally attach an owner.",
        "form": form,
        "back_url": "project_list",
        "back_label": "Back to Projects",
    }
    return render(request, "resources/form.html", context)


@login_required
def project_update(request, pk):
    project = get_object_or_404(Projects, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("project_list")
    else:
        form = ProjectForm(instance=project)

    context = {
        "page_title": "Edit Project",
        "eyebrow": "Project Space",
        "heading": "Edit Project",
        "description": "Update project ownership and current status.",
        "form": form,
        "back_url": "project_list",
        "back_label": "Back to Projects",
    }
    return render(request, "resources/form.html", context)


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Projects, pk=pk)
    if request.method == "POST":
        project.delete()
        return redirect("project_list")

    context = {
        "page_title": "Delete Project",
        "eyebrow": "Project Space",
        "heading": "Delete Project",
        "description": f"Delete '{project.name}' permanently.",
        "object_label": project.name,
        "back_url": "project_list",
        "back_label": "Back to Projects",
    }
    return render(request, "resources/delete.html", context)


@login_required
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = CourseForm()

    context = {
        "page_title": "Create Course",
        "eyebrow": "Course Catalog",
        "heading": "Create Course",
        "description": "Add a new course with a title and description.",
        "form": form,
        "back_url": "course_list",
        "back_label": "Back to Courses",
    }
    return render(request, "resources/form.html", context)


@login_required
def course_update(request, pk):
    course = get_object_or_404(Courses, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = CourseForm(instance=course)

    context = {
        "page_title": "Edit Course",
        "eyebrow": "Course Catalog",
        "heading": "Edit Course",
        "description": "Update course details and keep the catalog current.",
        "form": form,
        "back_url": "course_list",
        "back_label": "Back to Courses",
    }
    return render(request, "resources/form.html", context)


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Courses, pk=pk)
    if request.method == "POST":
        course.delete()
        return redirect("course_list")

    context = {
        "page_title": "Delete Course",
        "eyebrow": "Course Catalog",
        "heading": "Delete Course",
        "description": f"Delete '{course.title}' permanently.",
        "object_label": course.title,
        "back_url": "course_list",
        "back_label": "Back to Courses",
    }
    return render(request, "resources/delete.html", context)


@login_required
def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("subject_list")
    else:
        form = SubjectForm()

    context = {
        "page_title": "Create Subject",
        "eyebrow": "Subject Library",
        "heading": "Create Subject",
        "description": "Add a new subject for students, teachers, and courses.",
        "form": form,
        "back_url": "subject_list",
        "back_label": "Back to Subjects",
    }
    return render(request, "resources/form.html", context)


@login_required
def subject_update(request, pk):
    subject = get_object_or_404(Subjects, pk=pk)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect("subject_list")
    else:
        form = SubjectForm(instance=subject)

    context = {
        "page_title": "Edit Subject",
        "eyebrow": "Subject Library",
        "heading": "Edit Subject",
        "description": "Rename or adjust an existing subject entry.",
        "form": form,
        "back_url": "subject_list",
        "back_label": "Back to Subjects",
    }
    return render(request, "resources/form.html", context)


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subjects, pk=pk)
    if request.method == "POST":
        subject.delete()
        return redirect("subject_list")

    context = {
        "page_title": "Delete Subject",
        "eyebrow": "Subject Library",
        "heading": "Delete Subject",
        "description": f"Delete '{subject.title}' permanently.",
        "object_label": subject.title,
        "back_url": "subject_list",
        "back_label": "Back to Subjects",
    }
    return render(request, "resources/delete.html", context)
