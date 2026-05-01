from django.urls import include, path
from rest_framework import routers

from .views import StudentViewSet, student_list, student_create, student_delete, student_update

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('students_list/', student_list, name='student_list'),
    path('create_student/', student_create, name='student_create'),
    path('delete_student/<int:pk>', student_delete, name='student_delete'),
    path('update_student/<int:pk>', student_update, name='student_update'),
]
