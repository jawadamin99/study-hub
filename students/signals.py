from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .models import Student

print("signals loaded....!!!")


@receiver(pre_save, sender=Student)
def before_student_save(sender, instance, **kwargs):
    print("before student save", instance.first_name)


@receiver(post_save, sender=Student)
def after_student_save(sender, instance, created, **kwargs):
    print("after student save", instance.first_name)


@receiver(post_delete, sender=Student)
def after_student_delete(sender, instance, **kwargs):
    print("after student delete", instance.first_name)
