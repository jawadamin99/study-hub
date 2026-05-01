from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def assign_group_based_on_role(sender, instance, **kwargs):
    print("new user created, assignning group permission with signal!!!")
    role_group_names = {role.value for role in User.Role}
    group, _ = Group.objects.get_or_create(name=instance.role)

    old_role_groups = Group.objects.filter(name__in=role_group_names).exclude(name=instance.role)
    instance.groups.remove(*old_role_groups)
    instance.groups.add(group)
    print(f"old_role_groups", old_role_groups)
    print(f"new_group_applied", group.name)
