# NOT NEEDED NOW. PLEASE IGNORE!
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from.models import Profile
#
#
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     """
#     Signal for creating a new profile according to a new user that was created.
#     """
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     """
#     Signal for saving the created profile in the DB.
#     """
#     instance.profile.save()