from django.db import models

from user_auth.models import User


# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task'
        ordering = ['-created_on']


class RequestLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    path = models.TextField()
    method = models.TextField()
    execution_time = models.TextField()
    response_type = models.TextField(default='ok',blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.path

    class Meta:
        db_table = 'request_log'
        ordering = ['-timestamp']
