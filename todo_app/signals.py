from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from todo_app.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff == False or (instance.is_staff == False and instance.is_superuser == False):
            Profile.objects.create(user=instance)
