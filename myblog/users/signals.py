from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from.models import Profile


"""
Signal for creating a new profile according to a new user that was created.
"""
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


"""
Signal for saving the created profile in the DB.
"""
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()