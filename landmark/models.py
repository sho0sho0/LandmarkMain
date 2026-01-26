from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.crypto import get_random_string
import random
from django.db.models.signals import pre_save
import string
from django.db.models import Avg, Count

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Diploma(models.Model):
    # ONLINE_OFFLINE_CHOICES = [
    #     ('online', 'Online'),
    #     ('offline', 'Offline'),
    # ]

    # LEVEL_CHOICES = [
    #     ('beginner', 'Beginner'),
    #     ('intermediate', 'Intermediate'),
    #     ('advanced', 'Advanced'),
    # ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price_egp = models.DecimalField(max_digits=1000000, decimal_places=2, help_text="Price in Egyptian Pounds (EGP)", null=True, blank=True)
    price_usd = models.DecimalField(max_digits=1000000, decimal_places=2, help_text="Price in U.S. Dollars (USD)", null=True, blank=True)
    # content = models.TextField()
    # rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    image = models.ImageField(upload_to='diplomas/images',)
    # is_online = models.CharField(max_length=10, choices=ONLINE_OFFLINE_CHOICES, null=True)
    # level = models.CharField(max_length=20, choices=LEVEL_CHOICES, null=True)
    course_duration = models.DurationField() 
    course_duration_months = models.IntegerField(
    help_text="Course duration in months"
)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="diplomas")
    start_course = models.DateTimeField()
    end_course = models.DateTimeField() 
    instructor = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    sission_link = models.URLField(blank=True, null=True)
    module_count = models.IntegerField(editable=True, default=0)
    material_pdf = models.FileField(upload_to='diplomas/material', null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    

    def __str__(self):
        return self.name
    
    def total_sessions(self):
        total = 0
        for module in self.modules.all():
            total += module.session_count
        return total

    def update_module_count(self):
        self.module_count = self.modules.count()
        self.save()
    module_count.short_description = "Module Count"

    def average_rating(self):
        """
        Calculate the average rating of the diploma.
        Only approved ratings are considered.
        """
        return self.ratings.filter(is_approved=True).aggregate(Avg('score'))['score__avg'] or 0

    def ratings_count(self):
        """
        Count the number of ratings for the diploma.
        Only approved ratings are considered.
        """
        return self.ratings.filter(is_approved=True).count()
    
    def approved_comments(self):
        """
        Retrieve all approved comments for the diploma.
        """
        return self.comments.filter(is_approved=True)




class Module(models.Model):
    diploma = models.ForeignKey(Diploma, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255000) 
    duration = models.DurationField(blank=True, null=True)  
    instructor = models.CharField(max_length=255, blank=True, null=True)  
    sessions = models.TextField(blank=True, null=True, help_text="Write each bullet point on a new line.")
    # session_count = models.IntegerField(default=0, editable=True)
    link = models.URLField(blank=True, null=True)
    material_pdf = models.FileField(upload_to='diplomas/module/material', blank=True, null=True)
    instructor_image = models.ImageField(upload_to='instructors/',blank=True, null=True)


    @property
    def session_count(self):
        # Count the number of lines in the sessions field
        return len(self.sessions.splitlines()) if self.sessions else 0

    def formatted_sub_content(self):
        return self.sub_content.splitlines() 


    def __str__(self):
        return f"{self.diploma.name} - {self.title}"
    
# class Session(models.Model):
#     module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='sessions')
#     title = models.CharField(max_length=255000)
#     content = models.TextField(blank=True, null=True, help_text="Write each bullet point on a new line.")

#     def formatted_content(self):
#         return self.content.splitlines()

#     def __str__(self):
#         return f"{self.module.title} - {self.title}"



# Signal to automatically update module_count based on the number of lines in content
@receiver(post_save, sender=Module)
@receiver(post_delete, sender=Module)
def update_diploma_module_count(sender, instance, **kwargs):
    instance.diploma.update_module_count()
# Signal to automatically update session_count based on the number of lines in content
# @receiver(post_save, sender=Module)
# @receiver(post_delete, sender=Module)
# def update_module_session_count(sender, instance, **kwargs):
#     instance.update_session_count()

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='profiles/', blank=True, null=True)
#     diplomas_taken = models.ManyToManyField(Diploma, related_name="taken_by", blank=True)
#     wishlist = models.ManyToManyField(Diploma, related_name="wishlist_by", blank=True)
# def __str__(self):
#         return self.user.username



class UserProfile(models.Model):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True, )
    # diplomas_taken = models.ManyToManyField(Diploma, related_name="taken_by", blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    wishlist = models.ManyToManyField(Diploma, related_name="wishlist_by", blank=True)
    #email = models.EmailField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    # verification_token = models.CharField(max_length=32, blank=True, null=True)

    # def generate_verification_token(self):
    #     token = get_random_string(length=32)
    #     self.verification_token = token
    #     self.save()
    #     return token
    # def save(self, *args, **kwargs):
    #     # Sync the email field with the User model's email
    #     if self.user and self.user.email != self.email:
    #         self.email = self.user.email
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
def generate_username(first_name, last_name):
    random_numbers = ''.join(random.choices(string.digits, k=2))
    return f"{first_name.lower()}{last_name.lower()}{random_numbers}"

@receiver(pre_save, sender=User)
def create_username(sender, instance, **kwargs):
    if not instance.username:
        # Automatically generate the username based on first and last name
        first_name = instance.first_name
        last_name = instance.last_name
        instance.username = generate_username(first_name, last_name)
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and not hasattr(instance, 'userprofile'):
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     try:
#         instance.userprofile.save()
#     except UserProfile.DoesNotExist:
#         pass
# To ensure the UserProfile model’s email field is always updated whenever the User model’s email changes.  
# @receiver(post_save, sender=User)
# def update_user_profile_email(sender, instance, **kwargs):
#     if instance.userprofile:
#         instance.userprofile.email = instance.email
#         instance.userprofile.save()

class SelectedDiploma(models.Model):
    # MODE_CHOICES = [
    #     ('online', 'Online'),
    #     ('offline', 'Offline'),
    # ]
    

    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='selected_diplomas')
    diploma = models.ForeignKey(Diploma, on_delete=models.CASCADE, related_name='selected_by_users')
    # mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    taken_on = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def update_rating(self):
        approved_ratings = self.ratings.filter(is_approved=True)
        if approved_ratings.exists():
            self.rating = approved_ratings.aggregate(models.Avg('score'))['score__avg']
            self.save()


    # def __str__(self):
    #     return f"{self.user_profile.user.username} - {self.diploma.name} ({self.mode})"
    # class Meta:
    #     unique_together = ('user', 'diploma')  # Ensure a user can't take the same diploma twice


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    #diploma = models.ForeignKey(Diploma, on_delete=models.SET_NULL, null=True, blank=True)
    diploma = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback by {self.name} for {self.diploma}"


class Rating(models.Model):
    diploma = models.ForeignKey(Diploma, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=2, decimal_places=1)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Rating {self.score} by {self.user.username} for {self.diploma.name}"

class Comment(models.Model):
    diploma = models.ForeignKey(Diploma, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False) 

    def __str__(self):
        return f"Comment by {self.user.username} on {self.diploma.name}"


    
class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method_name = models.CharField(max_length=100)
    details = models.TextField()  # This can include card details and info.

    def __str__(self):
        return f"{self.method_name} for {self.user.username}"
    

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='events/')
    date = models.DateTimeField()

    def __str__(self):
        return self.title

from django.db import models

class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.email

class Partner(models.Model):
    company_name = models.CharField(max_length=255, )
    logo = models.ImageField(upload_to='partner/')

    def __str__(self):
        return self.company_name
    
class TrainingImage(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='training_images')
    image = models.ImageField(upload_to='partner/training/', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Training Image for {self.partner.company_name} - {self.title if self.title else 'No Title'}"
    
class Team(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team/')
    email_link = models.EmailField(max_length=255, blank=True, null=True)
    linkedin_link = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    
from django.db import models

class ContactUs(models.Model):
    email = models.EmailField(max_length=254, verbose_name="Email Address")
    name = models.CharField(max_length=100, verbose_name="Name")
    question = models.TextField(verbose_name="Your Question")
    phone = models.CharField(max_length=15, blank=True, null=True)
    diploma = models.ForeignKey(Diploma, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Us Entry"
        verbose_name_plural = "Contact Us Entries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"

class GraduationImages(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='graduation/')
    def __str__(self):
        return self.name

class TrainingGallery(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Training Gallery/')
    def __str__(self):
        return self.name
