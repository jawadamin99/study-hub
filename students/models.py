from django.contrib import auth
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


# Create your models here.
class Courses(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "courses"


class Subjects(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "subjects"


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField(default=30, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    courses = models.ManyToManyField(Courses, related_name='students', blank=True)
    subject = models.ForeignKey(Subjects, related_name='students', on_delete=models.CASCADE, null=True, blank=True,
                                default=None)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = 'students'


class Teachers(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True)
    age = models.IntegerField()
    email = models.EmailField(null=True)
    phone = models.IntegerField(null=True)
    subjects = models.ManyToManyField(Subjects, related_name='teachers', blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


def __str__(self):
    return f"{self.first_name} {self.last_name}"


class Meta:
    db_table = "teachers"


class Projects(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='projects', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "projects"
        permissions = [("can_publish_project", "Can publish project"),
                       ("can_archive_project", "Can archive project"), ]
