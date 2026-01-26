from django.db import IntegrityError
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Diploma, UserProfile, SelectedDiploma, Partner, Team, Comment, Rating, Subscription, Feedback, ContactUs, TrainingImage, GraduationImages, TrainingGallery
from .forms import UserSignupForm, UserLoginForm, UserProfileUpdateForm, UserUpdateForm, SelectDiplomaForm, UserPasswordChangeForm, RatingForm, CommentForm, FeedbackForm, SubscriptionForm
from django.contrib.auth import login
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlencode
import json
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import random
import re
from django.contrib.auth import authenticate, login as auth_login
from datetime import datetime
import logging
from django.core.files.storage import default_storage
from django.conf import settings
import os

# Home Function
def index(request):
    user_profile1 = request.user.userprofile if request.user.is_authenticated else None
    user_profiles_with_images = UserProfile.objects.filter(image__isnull=False).exclude(image='')
    random_profiles = random.sample(list(user_profiles_with_images), min(5, len(user_profiles_with_images)))
    partners = Partner.objects.all()
    teams = Team.objects.all()
    approved_comments = Comment.objects.filter(is_approved=True)[:20] 
    approved_ratings = Rating.objects.filter(is_approved=True)
    comments_with_ratings = []
    diplomas = Diploma.objects.all()
    training_images = TrainingImage.objects.all()
    user_profile1 = request.user.userprofile if request.user.is_authenticated else None
    graduation = GraduationImages.objects.all()
    training = TrainingGallery.objects.all()

    # def generate_random_color():
    #     return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    color_list = ['#FF5733', '#33FF57', '#3357FF', '#F4C542', '#E13B3B']

    for comment in approved_comments:
       
        rating = approved_ratings.filter(user=comment.user, diploma=comment.diploma).first()
        
        user_profile = UserProfile.objects.filter(user=comment.user).first()
        profile_image = user_profile.image.url if user_profile and user_profile.image else None
        rating_range = range(int(rating.score)) if rating else range(0)
        star_range = range(min(5, int(rating.score))) if rating else range(0)
        random_color = random.choice(color_list)
        
        
        comments_with_ratings.append({
            'comment': comment,
            'rating': rating,
            'rating_range': star_range,
            'profile_image': profile_image,
            'random_color': random_color,
            'user_profile':user_profile1
            # 'diplomas': diplomas
        })
        email = name = phone = question = None
        if request.method == 'POST':
            email = request.POST.get('email')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            program_id = request.POST.get('program')
            question = request.POST.get('question')

        if email and name and phone and question:
            try:
                program = Diploma.objects.get(id=program_id) if program_id else None
                contact = ContactUs.objects.create(
                    email=email,
                    name=name,
                    phone=phone,
                    diploma=program,
                    question=question,
                )
                contact.save()
                return render(request, 'landmark/home.html', {
                    'success': True,
                    'random_profiles': random_profiles,
                    'partners': partners,
                    'team_member': teams,
                    'comments_with_ratings': comments_with_ratings,
                    'diplomas': diplomas,
                    'training_images': training_images,
                    'user_profile1':user_profile1,
                    'graduation':graduation,
                    'training':training
                })
            except Diploma.DoesNotExist:
                messages.error(request, "The selected program doesn't exist.")
        else:
            messages.error(request, "Please fill in all required fields.")
    return render(request, 'landmark/home.html', {
        'error': True,
        'user_profile1': user_profile1,
        'random_profiles': random_profiles,
        'partners': partners,
        'team_member': teams,
        'comments_with_ratings': comments_with_ratings,
        'diplomas': diplomas,
        'training_images': training_images,
        'graduation':graduation,
        'training':training
        
    })
# SignUp Function
# def signup(request):
#     if request.method == 'POST':
#         form = UserSignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()  # Create the user from the form data
#             MyProfile.objects.get_or_create(user=user)
#             # try:
#             #     # Check if UserProfile already exists, and create if it doesn't
#             #     UserProfile.objects.get_or_create(user=user)
#             # except IntegrityError:
#             #     # If the user already has a profile, do nothing
#             #     pass
            
#             # Log the user in after successful signup
#             login(request, user)
            
#             # Redirect to the profile page or a dashboard
#             return redirect('profile')  # You can change 'profile' to the actual URL name
            
#     else:
#         form = UserSignupForm()  # Instantiate the signup form
    
#     return render(request, 'landmark/signup.html', {'form': form})

# SignUp Function
# def signup(request):
#     if request.method == 'POST':
#         form = UserSignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Check if UserProfile already exists
#             UserProfile.objects.get_or_create(user=user)  # Create UserProfile only if it does not exist
#             login(request, user)
#             return redirect('profile') 
#     else:
#         form = UserSignupForm()
#     return render(request, 'landmark/signup.html', {'form': form})

def validate_name(name, field_name):
    """Validates that the name contains only letters and no spaces."""
    name = name.strip()
    if not re.match('^[a-zA-Z]+$', name):
        raise ValidationError(f"{field_name} must contain only letters and no spaces.")
    return name

# SignUp Function
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first-name', '').strip()
        last_name = request.POST.get('last-name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            # Validate first and last name
            first_name = validate_name(first_name, "First name")
            last_name = validate_name(last_name, "Last name")

            # Generate a unique username
            base_username = f"{first_name.lower()}{last_name.lower()}"
            username = base_username + str(random.randint(10, 99))
            while User.objects.filter(username=username).exists():
                username = base_username + str(random.randint(100, 999))

            # Create user and user profile
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )

            UserProfile.objects.create(
                user=user,
                full_name=f"{first_name} {last_name}",
                phone_number=phone
            )

            # Log in the user
            auth_login(request, user)

            # Add success message
            messages.success(request, f"Your account has been successfully created. Welcome, {username}!")

            return redirect('profile')

        except ValidationError as e:
            messages.error(request, e.message)
        except Exception as e:
            messages.error(request, "An error occurred while creating your account. Please try again later.")

    return render(request, 'landmark/signup.html')

   


# Login Function
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')
        remember_me = 'remember_me' in request.POST

        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            
            auth_login(request, user)

            # If Remember Me is checked, store username and password in the session
            if remember_me:
                request.session['username'] = username
                request.session['remember_me'] = True
            else:
                # Clear the session if Remember Me is not checked
                if 'username' in request.session:
                    del request.session['username']
                if 'remember_me' in request.session:
                    del request.session['remember_me']

            messages.success(request, "You have logged in successfully!")
            return redirect('profile')  

        else:
            messages.error(request, "Invalid credentials, please try again.")

    return render(request, 'landmark/login.html')


# LogOut Function
def logout_view(request):
    logout(request)
    return redirect('index')


# User Profile Function
@login_required
def user_profile(request):
    user_profile1 = request.user.userprofile if request.user.is_authenticated else None
    user_profile = request.user.userprofile
    user = request.user
    profile = user.userprofile 
    profile_image_url = (
        user_profile.image.url 
        if user_profile.image 
        else settings.STATIC_URL + 'landmark/images/user1.png'
    )

    now = datetime.now()

    selected_diplomas = SelectedDiploma.objects.filter(
        user_profile=user_profile,
        diploma__end_course__gte=now,
        is_approved=True
    )
    wishlist_diplomas = user_profile.wishlist.all()
    if request.method == "POST" and request.user.is_authenticated:
        diploma_id = request.POST.get('diploma_id')
        action = request.POST.get('action')
        user_profile = UserProfile.objects.get(user=request.user)
        
        try:
            diploma = Diploma.objects.get(id=diploma_id)
            
            if action == 'remove':
                user_profile.wishlist.remove(diploma)  # Add diploma to wishlist
              # Remove diploma from wishlist
            user_profile.save()
        except Diploma.DoesNotExist:
            pass 

        # Return a response indicating whether the diploma was added or removed
        
    comment_submitted = False
    if request.method == 'POST':
        if 'comment' in request.POST:  # Check if the comment form was submitted
            comment_content = request.POST.get('comment')
            diploma_id = request.POST.get('diploma_id')
            diploma = get_object_or_404(SelectedDiploma, id=diploma_id, user_profile=user_profile).diploma

            if comment_content:
                Comment.objects.create(
                    diploma=diploma,
                    user=user,
                    content=comment_content
                )
                comment_submitted = True


    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')

        if email:
            user.email = email
        if phone_number:
            profile.phone_number = phone_number
            profile.save()

        if password:
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)  

        user.save()
        return redirect('profile') 
    return render(request, 'landmark/my_profile.html', {
        'user_profile1': user_profile1,
        'user_profile': user_profile,
        'profile': profile,
        'selected_diplomas': selected_diplomas,
        'comment_submitted': comment_submitted,
        'profile_image_url': profile_image_url,
        'wishlist_diplomas': wishlist_diplomas
    })

@csrf_exempt
@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        user_profile = request.user.userprofile

        # Limit the file size (e.g., 2MB)
        max_size = 4 * 1024 * 1024  # 2 MB
        if image.size > max_size:
            return JsonResponse({'success': False, 'message': 'Image exceeds the maximum size of 4MB.'}, status=400)

        # Delete the old image if exists and not the default one
        if user_profile.image and user_profile.image.name != 'landmark/images/user1.png':
            old_image_path = user_profile.image.path
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        # Save the new image
        user_profile.image = image
        user_profile.save()

        return JsonResponse({
            'success': True,
            'new_image_url': user_profile.image.url
        })
    return JsonResponse({'success': False, 'message': 'No image uploaded'}, status=400)

# @login_required
# def user_profile(request):
    # if request.method == 'POST':
    #     # Updating the info.
    #     user_form = UserUpdateForm(request.POST, instance=request.user)
    #     profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
    #     password_form = PasswordChangeForm(request.user, request.POST)

    #     if user_form.is_valid() and profile_form.is_valid():
    #         user_form.save()
    #         profile_form.save()
    #         messages.success(request, 'Your profile has been updated!')
    #         return redirect('profile')

    #     elif password_form.is_valid():
    #         user = password_form.save()
    #         update_session_auth_hash(request, user)  # Keeps the user logged in after password change
    #         messages.success(request, 'Your password has been updated!')
    #         return redirect('profile')
#     else:
#         user_form = UserUpdateForm(instance=request.user)
#         profile_form = UserProfileUpdateForm(instance=request.user.userprofile)
#         password_form = PasswordChangeForm(request.user)

#         # Fetching diplomas taken by the user's profile
#         selected_diplomas = SelectedDiploma.objects.filter(user_profile=request.user.userprofile)

#     return render(request, 'landmark/my_profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'password_form': password_form,
#         'selected_diplomas': selected_diplomas,
#     })
# @login_required
# def user_profile(request):
#     if request.method == 'POST':
#         # Updating the info.
#         user_form = UserUpdateForm(request.POST, instance=request.user)
#         profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
#         password_form = PasswordChangeForm(request.user, request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile has been updated!')
#             return redirect('profile')

#         elif password_form.is_valid():
#             user = password_form.save()
#             update_session_auth_hash(request, user)  # Keeps the user logged in after password change
#             messages.success(request, 'Your password has been updated!')
#             return redirect('profile')
#     else:
#         user_form = UserUpdateForm(instance=request.user)
#         profile_form = UserProfileUpdateForm(instance=request.user.userprofile)
#         password_form = PasswordChangeForm(request.user)

#         # Fetch only diplomas that haven't expired
#         now = datetime.now()
#         selected_diplomas = SelectedDiploma.objects.filter(
#             user_profile=request.user.userprofile,
#             diploma__end_course__gte=now,
#             is_approved=True
#         )

#     return render(request, 'landmark/my_profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'password_form': password_form,
#         'selected_diplomas': selected_diplomas,
#     })

# @login_required
# def user_profile(request):
#     if request.method == 'POST':
#         # Handling user update
#         user_form = UserUpdateForm(request.POST, instance=request.user)
#         profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

#         # Password change form
#         password_form = UserPasswordChangeForm(user=request.user, data=request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()

#             # Handle password change if the password form is valid
#             if password_form.is_valid():
#                 user = password_form.save()
#                 update_session_auth_hash(request, user)  # Keep the user logged in
#                 return redirect('profile')  # Redirect after saving
            
#             return redirect('profile')  # Redirect after updating user profile

#     else:
#         user_form = UserUpdateForm(instance=request.user)
#         profile_form = UserProfileUpdateForm(instance=request.user.userprofile)
#         password_form = UserPasswordChangeForm(user=request.user)

#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'password_form': password_form,
#     }
#     return render(request, 'landmark/my_profile.html', context)

# Diplomas Function
def diploma_list(request, ):
    user_profile1 = request.user.userprofile if request.user.is_authenticated else None
    diplomas = Diploma.objects.exclude(category__name="Mini MBA")

    # Add modules_count and cy values for each diploma
    for diploma in diplomas:
        diploma.modules_count = diploma.modules.count()
        diploma.modules_height = 100 * diploma.modules_count  
        diploma.module_positions = [100 * i for i in range(1, diploma.modules_count + 1)] 
        diploma.modules_list = list(diploma.modules.all())


    if request.method == "POST" and request.user.is_authenticated:
        diploma_id = request.POST.get('diploma_id')
        action = request.POST.get('action')
        user_profile = UserProfile.objects.get(user=request.user)
        
        try:
            diploma = Diploma.objects.get(id=diploma_id)
            
            if action == 'add':
                user_profile.wishlist.add(diploma)  
            elif action == 'remove':
                user_profile.wishlist.remove(diploma)  
            user_profile.save()
        except Diploma.DoesNotExist:
            pass 
    # diplomas = Diploma.objects.all()
    # for diploma in diplomas:
    #     diploma.update_module_count()  # Update module count for each diploma
    #     diploma.module_range = range(diploma.module_count)
    return render(request, 'landmark/diploma_list.html', {
        'diplomas': diplomas,
        'user_profile1':user_profile1,
      
        
        })

# Mini MBA Function
def mini_mba(request):
    user_profile1 = request.user.userprofile if request.user.is_authenticated else None
    masters = Diploma.objects.filter(category__name="Mini MBA")

    for master in masters:
        master.total_sessions_count = master.total_sessions()
        master.approved_comments = master.comments.filter(is_approved=True)
    return render(request, "landmark/mini_mba.html", {
        "masters":masters,
        'user_profile1':user_profile1,
    })

# Enroll Diploma Function
logger = logging.getLogger(__name__)
@login_required
def enroll_diploma(request, diploma_id):
    if request.method == 'POST':
        # try:
        #     data = json.loads(request.body)
        #     mode = data.get('mode')
        # except (json.JSONDecodeError, KeyError):
        #     return JsonResponse({'error': 'Invalid data'}, status=400)

        # if mode not in ['online', 'offline']:
        #     return JsonResponse({'error': 'Invalid mode'}, status=400)

        diploma = get_object_or_404(Diploma, id=diploma_id)
        SelectedDiploma.objects.create(
            user_profile=request.user.userprofile,
            diploma=diploma,
            # mode=mode
        )
        return JsonResponse({'message': 'Diploma enrolled successfully!'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Enroll Mini MBA Function
@login_required
def enroll_minimba(request, diploma_id):
    if request.method == 'POST':
        # try:
        #     data = json.loads(request.body)
        #     mode = data.get('mode')
        # except (json.JSONDecodeError, KeyError):
        #     return JsonResponse({'error': 'Invalid data'}, status=400)

        # if mode not in ['online', 'offline']:
        #     return JsonResponse({'error': 'Invalid mode'}, status=400)

        diploma = get_object_or_404(Diploma, id=diploma_id)
        SelectedDiploma.objects.create(
            user_profile=request.user.userprofile,
            diploma=diploma,
            # mode=mode
        )
        return JsonResponse({'message': 'Diploma enrolled successfully!'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# Add To Favorites Function



# @login_required
# def add_to_wishlist(request, diploma_id):
#     diploma = get_object_or_404(Diploma, id=diploma_id)
    
#     # Get or create UserProfile for the current user
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
#     if diploma in user_profile.wishlist.all():
#         return JsonResponse({'success': False, 'message': 'This diploma is already in your wishlist.'})
    
#     user_profile.wishlist.add(diploma)
#     return JsonResponse({'success': True, 'message': 'Diploma added to your wishlist.'})

# # Remove From Favorites Function
# @csrf_exempt
# @login_required
# def remove_from_wishlist(request, diploma_id):
#     diploma = get_object_or_404(Diploma, id=diploma_id)
    
#     # Get or create UserProfile for the current user
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
#     if diploma not in user_profile.wishlist.all():
#         return JsonResponse({'success': False, 'message': 'This diploma is not in your wishlist.'})

#     user_profile.wishlist.remove(diploma)
#     return JsonResponse({'success': True, 'message': 'Diploma removed from your wishlist.'})

# Diploma Details Function
# def diploma_detail(request, diploma_id):
#     diploma = get_object_or_404(Diploma, id=diploma_id)
#     return render(request, 'landmark/diploma_detail.html', {'diploma': diploma})

# Take Diploma Function
# @login_required
# def take_diploma(request, diploma_id):
#     diploma = get_object_or_404(Diploma, id=diploma_id)
    
#     if request.method == 'POST':
#         online_offline = request.POST.get('online_offline')
#         user_profile, created = UserProfile.objects.get_or_create(user=request.user)

#         if online_offline in dict(Diploma.ONLINE_OFFLINE_CHOICES):
#             user_profile.diplomas_taken.add(diploma)
#             messages.success(request, f"You have successfully taken the {diploma.name} diploma as {online_offline}.")
#         else:
#             messages.error(request, "Invalid selection.")
        
#         return redirect('profile')   Redirect to user profile or any desired page

#     return render(request, 'landmark/take_diploma.html', {'diploma': diploma})
# @login_required
# def take_diploma(request, diploma_id):
#     diploma = get_object_or_404(Diploma, id=diploma_id)
#     if request.method == 'POST':
#         form = SelectDiplomaForm(request.POST)
#         if form.is_valid():
#             selected_diploma = form.save(commit=False)
#             selected_diploma.user = request.user
#             selected_diploma.diploma = diploma
#             selected_diploma.save()
#             return redirect('profile')
#     else:
#         form = SelectDiplomaForm()
#     return render(request, 'landmark/take_diploma.html', {'form': form, 'diploma': diploma})




# @login_required
# def take_diploma(request, diploma_id):
#     diploma = get_object_or_404(Diploma, id=diploma_id)
#     user_profile = UserProfile.objects.get(user=request.user)

#     if request.method == "POST":
#         form = SelectDiplomaForm(request.POST)
#         if form.is_valid():
#             selected_diploma = form.save(commit=False)
#             selected_diploma.user_profile = user_profile
#             selected_diploma.diploma = diploma
#             selected_diploma.taken_on = timezone.now()  
#             selected_diploma.save()
#             messages.success(request, f"You have successfully enrolled in {diploma.name}!")
#             return redirect('diploma_detail', diploma_id=diploma_id)
#     else:
#         form = SelectDiplomaForm()

#     return render(request, 'landmark/take_diploma.html', {'form': form, 'diploma': diploma})

# Comments & Rating Function
# def diploma_detail(request, diploma_id):
#     diploma = get_object_or_404(Diploma, id=diploma_id)
#     comments = diploma.comments.filter(is_approved=True)
#     ratings = diploma.ratings.filter(is_approved=True)

#     comment_form = CommentForm()
#     rating_form = RatingForm()

#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             comment_form = CommentForm(request.POST)
#             rating_form = RatingForm(request.POST)

#             if comment_form.is_valid() and rating_form.is_valid():
#                 # Save the comment
#                 comment = comment_form.save(commit=False)
#                 comment.diploma = diploma
#                 comment.user = request.user
#                 comment.save()

#                 # Save the rating
#                 rating = rating_form.save(commit=False)
#                 rating.diploma = diploma
#                 rating.user = request.user
#                 rating.save()

#                 messages.success(request, 'Your comment and rating have been submitted and are awaiting approval.')
#                 return redirect('diploma_detail', diploma_id=diploma_id)
#             else:
#                 messages.error(request, 'There was an error with your comment or rating.')
#         else:
#             messages.error(request, 'You need to log in to submit a comment or rating.')
#             return redirect('login')  # Redirect to login page if the user is not authenticated

#     return render(request, 'landmark/diploma_detail.html', {'diploma': diploma,
#         'comments': comments,
#         'ratings': ratings,
#         'comment_form': comment_form,
#         'rating_form': rating_form,})

# Feedback Function
# def feedback_view(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             form.save() 
#             return redirect('thank_you') 
#     else:
#         form = FeedbackForm()
#     return render(request, 'landmark/feedback.html', {'form': form})

# def thank_you(request):
#     return render(request, 'landmark/thank_you.html')

# FeedBack Function
def feedback_view(request):
    user_profile1 = request.user.userprofile if request.user.is_authenticated else None
    if request.method == 'POST':
        name = request.POST.get('name')
        diploma = request.POST.get('program')  # Map the "program" field to Diploma
        rating = request.POST.get('rate')
        comment = request.POST.get('comment')

        if name and diploma and rating and comment:
            try:
                # diploma = Diploma.objects.get(id=diploma_id)
                feedback = Feedback.objects.create(
                    name=name,
                    diploma=diploma,
                    rating=rating,
                    comment=comment,
                )
                feedback.save()
                return render(request, 'landmark/feedback.html', {'success': True})
            except Diploma.DoesNotExist:
                messages.error(request, "The selected diploma doesn't exist.")
        else:
            return render(request, 'landmark/feedback.html', {'error': True})

    diplomas = Diploma.objects.all()  # Pass diplomas to populate the dropdown
    return render(request, 'landmark/feedback.html', {
                      'diplomas': diplomas,
                      'user_profile1':user_profile1
                   })

# Subscription Function
# def subscribe_view(request):
#     if request.method == 'POST':
#         form = SubscriptionForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the email to the database
#             messages.success(request, "Thank you for subscribing!")
#             return redirect('thank_you') 
#         else:
#             messages.error(request, "Please provide a valid email address.")
#     else:
#         form = SubscriptionForm()

#     return render(request, 'landmark/subscribe.html', {'form': form})
@csrf_exempt  # Disable CSRF protection for this view, or use CSRF token in JavaScript
def subscribe(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if email:
                # Check if the email is already subscribed
                if Subscription.objects.filter(email=email).exists():
                    return JsonResponse({'message': 'Already subscribed'}, status=400)
                
                # Create a new subscription
                Subscription.objects.create(email=email)
                return JsonResponse({'message': 'Successfully subscribed'}, status=201)
            else:
                return JsonResponse({'message': 'Email is required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid data'}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=405)



def validate_email(email):
    email_validator = EmailValidator()
    try:
        email_validator(email)
    except ValidationError:
        raise ValidationError("Invalid email format")



# Contact Us Entiers Function
def contact_us_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        program = request.POST.get('program')  
        question = request.POST.get('question')

        if email and name and phone and program and question:
            try:
                diploma = Diploma.objects.get(id=program)  
                contact_query = ContactUs.objects.create(
                    email=email,
                    name=name,
                    phone=phone,
                    diploma=diploma,
                    question=question
                )
                contact_query.save()
                return render(request, 'landmark/home.html', {'success': True})  
            except Diploma.DoesNotExist:
                messages.error(request, "The selected diploma doesn't exist.")
        else:
            return render(request, 'landmark/home.html', {'error': True})

    diplomas = Diploma.objects.all()  
    return render(request, 'landmark/home.html', {'diplomas': diplomas})

# About Function
def about(request):
    user_profile1 = request.user.userprofile if request.user.is_authenticated else None
    return render(
        request, 'landmark/aboutus.html',{
            'user_profile1':user_profile1})
# Training Function
def training(request):
    user_profile1 = request.user.userprofile if request.user.is_authenticated else None
    partners = Partner.objects.filter(training_images__isnull=False).distinct()

    training_images = {}
    for partner in partners:
        training_images[partner] = TrainingImage.objects.filter(partner=partner)
    return render(
        request, 'landmark/training.html',{
            'user_profile1':user_profile1,
            'partners': partners,
            'training_images': training_images,
            })
# Consulting Function
def consulting(request):
    user_profile1 = request.user.userprofile if request.user.is_authenticated else None
    return render(
        request, 'landmark/consulting.html',{
            'user_profile1':user_profile1})
# Assesment Function
def assesment(request):
    user_profile1 = request.user.userprofile if request.user.is_authenticated else None
    return render(
        request, 'landmark/assesment.html',{
            'user_profile1':user_profile1})
