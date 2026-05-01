"""
URL configuration for study_hub4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from students.views import (
    course_create,
    course_delete,
    course_list,
    course_update,
    ProjectViewSet,
    project_create,
    project_delete,
    project_list,
    project_update,
    subject_create,
    subject_delete,
    subject_list,
    subject_update,
)
from tasks.views import (
    NotificationViewSet,
    TaskViewSet,
    notification_list,
    notification_mark_read,
    task_create,
    task_delete,
    task_list,
    task_update,
)
from user_auth.views import UsersViewSet, MyTokenObtainPairView

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('students.urls')),
    path('api/tasks_list/', task_list, name='task_list'),
    path('api/tasks/create/', task_create, name='task_create'),
    path('api/tasks/<int:pk>/update/', task_update, name='task_update'),
    path('api/tasks/<int:pk>/delete/', task_delete, name='task_delete'),
    path('api/notifications_list/', notification_list, name='notification_list'),
    path('api/notifications/<int:pk>/mark-read/', notification_mark_read, name='notification_mark_read'),
    path('api/projects_list/', project_list, name='project_list'),
    path('api/projects/create/', project_create, name='project_create'),
    path('api/projects/<int:pk>/update/', project_update, name='project_update'),
    path('api/projects/<int:pk>/delete/', project_delete, name='project_delete'),
    path('api/courses_list/', course_list, name='course_list'),
    path('api/courses/create/', course_create, name='course_create'),
    path('api/courses/<int:pk>/update/', course_update, name='course_update'),
    path('api/courses/<int:pk>/delete/', course_delete, name='course_delete'),
    path('api/subjects_list/', subject_list, name='subject_list'),
    path('api/subjects/create/', subject_create, name='subject_create'),
    path('api/subjects/<int:pk>/update/', subject_update, name='subject_update'),
    path('api/subjects/<int:pk>/delete/', subject_delete, name='subject_delete'),
    path('api/', include(router.urls)),
    path('login/', MyTokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('user_login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
