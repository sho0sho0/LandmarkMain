
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile, Diploma, SelectedDiploma, Comment, Rating, Feedback, Subscription
from django.contrib.auth.forms import AuthenticationForm
import re
from django.core.exceptions import ValidationError


# SignUp Form
# class UserSignupForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     phone_number = forms.CharField(max_length=15, required=True)
#     first_name = forms.CharField(max_length=30, required=True, label="First Name")
#     last_name = forms.CharField(max_length=30, required=True, label="Last Name")
#     full_name = forms.CharField(max_length=255, required=True, label="Full Name")  # Optional if using full name as a single field

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone_number')

#     def save(self, commit=True):
#         user = super().save(commit=False)  # Save the user without committing to add custom fields
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()  # Now commit the user to the database
#             user_profile, created = UserProfile.objects.get_or_create(user=user)
#             user_profile.phone_number = self.cleaned_data['phone_number']
#             user_profile.save()  # Save the UserProfile data
#         return user

# class UserSignupForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     phone_number = forms.CharField(max_length=15, required=True)
#     full_name = forms.CharField(max_length=255, required=True, label="Full Name")

#     class Meta:
#         model = User
#         fields = ('full_name', 'username', 'email', 'password1', 'password2', 'phone_number')

#     def save(self, commit=True):
#         user = super().save(commit)  # Save the user first
#         # Ensure user profile is created after the user is saved
#         user_profile, created = UserProfile.objects.get_or_create(user=user)
#         user_profile.phone_number = self.cleaned_data['phone_number']
#         user_profile.save()  # Save the profile
#         return user

class UserSignupForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
    )
    phone_number = forms.CharField(
        label="Phone Number",
        max_length=15,
        required=True,
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# LogIn Form
class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

# Update Profile Info
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'phone_number']

# Update Profile Pass
class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

# Selected Diploma Form "mode" & "level"
class SelectDiplomaForm(forms.ModelForm):
    class Meta:
        model = SelectedDiploma
        fields = [ ]
        widgets = {
            # 'mode': forms.RadioSelect,
            
        }

# Diploma Form For Admin Panel
# class DiplomaAdminForm(forms.ModelForm):
#    class Meta:
#        model = Diploma
#        fields = '__all__'
    
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        # Only make fields optional if the object is being created
#        if not self.instance.pk:
#            self.fields['level'].required = False
#            self.fields['is_online'].required = False
            

# Feedback Form
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'diploma', 'rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

# Comments Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
        }

# Rting Form
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.1}),
        }

# Subscription Form
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']  # Only the email field will be included in the form

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # You can add custom validation here if needed, e.g. checking if the email is already subscribed
        return email
