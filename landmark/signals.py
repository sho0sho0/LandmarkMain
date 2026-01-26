# landmark/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
import random

# @receiver(post_save, sender=User)
# def update_user_profile_email(sender, instance, created, **kwargs):
#     if created:  # Only create the profile if the user is newly created
#         try:
#             # Create the user profile when the user is created
#             UserProfile.objects.create(user=instance)
#         except Exception as e:
#             print(f"Error creating user profile: {e}")

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         # Generate a unique username
#         random_number = random.randint(10, 99)
#         username = f"{instance.first_name.lower()}{instance.last_name.lower()}{random_number}"
#         while User.objects.filter(username=username).exists():
#             random_number = random.randint(10, 99)
#             username = f"{instance.first_name.lower()}{instance.last_name.lower()}{random_number}"

#         # Update the user's username
#         instance.username = username
#         instance.save()

#         # Create the UserProfile
#         full_name = f"{instance.first_name} {instance.last_name}"
#         UserProfile.objects.create(user=instance, full_name=full_name)
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         # Custom logic to generate username (handled in view already)
#         pass

#         # Create the UserProfile if not created manually in the view
#         if not hasattr(instance, 'userprofile'):
#             UserProfile.objects.create(user=instance, full_name=f"{instance.first_name} {instance.last_name}")