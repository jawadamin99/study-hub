from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Notification, Task


@receiver(post_save, sender=Task)
def log_task_created(sender, instance, created, **kwargs):
    if created:
        print(f"Task created: {instance.title}")
        Notification.objects.create(
            user=instance.assigned_to,
            task=instance,
            message=f"You have been assigned task: {instance.title}",
        )


@receiver(pre_save, sender=Task)
def track_task_changes(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_task = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    fields_to_track = ["title", "description", "is_active", "assigned_to", "created_by"]

    for field in fields_to_track:
        old_value = getattr(old_task, field)
        new_value = getattr(instance, field)

        if old_value != new_value:
            print(f"Task changed: {field} from {old_value} to {new_value}")

    if old_task.is_active and not instance.is_active:
        print(f"Task completed: {instance.title}")

    if old_task.assigned_to != instance.assigned_to:
        Notification.objects.create(
            user=instance.assigned_to,
            task=instance,
            message=f"You have been assigned task: {instance.title}",
        )
        print(f"Task reassigned to: {instance.assigned_to.email}")
