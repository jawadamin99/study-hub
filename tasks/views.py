from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .forms import TaskForm
from .models import Notification, Task
from .permissions import IsManagerOrReadOnly
from .serializers import NotificationSerializer, TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name__in=("Manager", "Admin")).exists():
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name__in=("Manager", "Admin")).exists():
            return Notification.objects.all()
        return Notification.objects.filter(user=user)


@login_required
def task_list(request):
    if request.user.groups.filter(name__in=("Manager", "Admin")).exists():
        tasks = Task.objects.select_related("project", "assigned_to", "created_by").all()
    else:
        tasks = Task.objects.select_related("project", "assigned_to", "created_by").filter(assigned_to=request.user)

    rows = [
        {
            "cells": [
                task.title,
                task.description,
                task.project.name if task.project else "No project",
                task.assigned_to.email,
                task.created_by.email,
                "Active" if task.is_active else "Inactive",
            ],
            "edit_url": "task_update",
            "delete_url": "task_delete",
            "pk": task.pk,
        }
        for task in tasks
    ]
    context = {
        "page_title": "Tasks",
        "eyebrow": "Task Board",
        "heading": "Tasks",
        "description": "Review task ownership, activity state, and who created each work item.",
        "columns": ["Title", "Description", "Project", "Assigned To", "Created By", "Status"],
        "rows": rows,
        "create_url": "task_create",
        "create_label": "Create Task",
    }
    return render(request, "resources/list.html", context)


@login_required
def notification_list(request):
    if request.user.groups.filter(name__in=("Manager", "Admin")).exists():
        notifications = Notification.objects.select_related("user", "task").all()
    else:
        notifications = Notification.objects.select_related("user", "task").filter(user=request.user)

    rows = [
        {
            "cells": [
                notification.message,
                notification.task.title,
                notification.user.email,
                "Read" if notification.is_read else "Unread",
                notification.created_on,
            ],
            "actions": [
                {
                    "label": "Mark read",
                    "url": "notification_mark_read",
                    "pk": notification.pk,
                    "class": "",
                }
            ] if not notification.is_read else [],
        }
        for notification in notifications
    ]
    context = {
        "page_title": "Notifications",
        "eyebrow": "Inbox",
        "heading": "Notifications",
        "description": "Review task assignment and reassignment alerts.",
        "columns": ["Message", "Task", "User", "Status", "Created"],
        "rows": rows,
    }
    return render(request, "resources/list.html", context)


@login_required
def notification_mark_read(request, pk):
    if request.user.groups.filter(name__in=("Manager", "Admin")).exists():
        notification = get_object_or_404(Notification, pk=pk)
    else:
        notification = get_object_or_404(Notification, pk=pk, user=request.user)

    notification.is_read = True
    notification.save()
    return redirect("notification_list")


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()

    context = {
        "page_title": "Create Task",
        "eyebrow": "Task Board",
        "heading": "Create Task",
        "description": "Add a new task and define who owns it and who created it.",
        "form": form,
        "back_url": "task_list",
        "back_label": "Back to Tasks",
    }
    return render(request, "resources/form.html", context)


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    context = {
        "page_title": "Edit Task",
        "eyebrow": "Task Board",
        "heading": "Edit Task",
        "description": "Update task details, assignment, and activity state.",
        "form": form,
        "back_url": "task_list",
        "back_label": "Back to Tasks",
    }
    return render(request, "resources/form.html", context)


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    context = {
        "page_title": "Delete Task",
        "eyebrow": "Task Board",
        "heading": "Delete Task",
        "description": f"Delete '{task.title}' permanently.",
        "object_label": task.title,
        "back_url": "task_list",
        "back_label": "Back to Tasks",
    }
    return render(request, "resources/delete.html", context)
