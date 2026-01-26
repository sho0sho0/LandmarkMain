# from django.contrib import admin
# from .models import Diploma, UserProfile, Comment, Category, PaymentMethod, SelectedDiploma

# # Diploma Admin Panel
# class DiplomaAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'price', 'rating', 'level', 'calendar', 'link')
#     list_filter = ('level', 'category')  
#     search_fields = ('name', 'description')
#     ordering = ('name',)

# # Comments Admin Panel
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('diploma', 'user', 'content', 'created_at', 'is_approved')
#     list_filter = ('is_approved', 'created_at')
#     search_fields = ('content',)
#     actions = ['approve_comments', 'reject_comments']

#     @admin.action(description='Approve selected comments')
#     def approve_comments(self, request, queryset):
#         queryset.update(is_approved=True)

#     @admin.action(description='Reject selected comments')
#     def reject_comments(self, request, queryset):
#         queryset.update(is_approved=False)

# # Wishlist of Diplomas Inline
# class WishDiplomaInline(admin.TabularInline):
#     model = UserProfile.wishlist.through
#     extra = 0
#     verbose_name = "Wishlist Diploma"
#     verbose_name_plural = "Wishlist Diplomas"

# # Taken Diplomas Inline for UserDiplomaSelection
# class TakenDiplomaInline(admin.TabularInline):
#     model = UserDiploma
#     extra = 0
#     fields = ('diploma', 'mode', 'level', 'date_taken')
#     readonly_fields = ('date_taken',)
#     verbose_name = "Selected Diploma"
#     verbose_name_plural = "Selected Diplomas"

# # User Profile Admin Panel
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'email', 'wishlist_count', 'taken_count')
#     search_fields = ('user__username', 'user__email')
#     ordering = ('user',)
#     inlines = [WishDiplomaInline, TakenDiplomaInline]

#     def email(self, obj):
#         return obj.user.email if obj.user else "No email"

#     email.short_description = "Email"

#     def wishlist_count(self, obj):
#         return obj.wishlist.count()

#     wishlist_count.short_description = "Wishlist Count"

#     def taken_count(self, obj):
#         return UserDiploma.objects.filter(user=obj.user).count()
#     taken_count.short_description = 'Number of Taken Diplomas'

#     def diplomas_taken(self, obj):
#         diplomas = UserDiploma.objects.filter(user=obj.user)
#         return ", ".join([f"{d.diploma.name} ({d.mode}, {d.level})" for d in diplomas])
#     diplomas_taken.short_description = "Selected Diplomas"

# # Diplomas Categories Admin Panel
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)

# # Payment Method Admin Panel
# class PaymentMethodAdmin(admin.ModelAdmin):
#     list_display = ('user', 'method_name')
#     search_fields = ('user__username', 'method_name')

# # Selected Diplomas Admin
# class UserDiplomaAdmin(admin.ModelAdmin):
#     list_display = ('user', 'diploma', 'mode', 'level', 'date_taken')
#     list_filter = ('mode', 'level', 'diploma')
#     search_fields = ('user__username', 'diploma__name')
#     ordering = ('user',)

# # Register the models and customize admin display
# admin.site.register(Diploma, DiplomaAdmin)
# admin.site.register(Comment, CommentAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(PaymentMethod, PaymentMethodAdmin)
# admin.site.register(UserDiploma, UserDiplomaAdmin)


# # Admin site branding
# admin.site.site_header = "Diploma Management Admin"
# admin.site.site_title = "Diploma Admin Portal"
# admin.site.index_title = "Welcome to the Diploma Management Admin"






# from django.contrib import admin
# from .models import Diploma, UserProfile, Comment, Category, PaymentMethod, SelectedDiploma

# # Diploma Panel
# class DiplomaAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'price', 'rating', 'is_online', 'level', 'calendar', 'link')
#     list_filter = ('is_online', 'level', 'category')
#     search_fields = ('name', 'description')
#     ordering = ('name',)

# # Comments Management
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('diploma', 'user', 'content', 'created_at', 'is_approved')
#     list_filter = ('is_approved', 'created_at')
#     search_fields = ('content',)
#     actions = ['approve_comments', 'reject_comments']

#     @admin.action(description='Approve selected comments')
#     def approve_comments(self, request, queryset):
#         queryset.update(is_approved=True)

#     @admin.action(description='Reject selected comments')
#     def reject_comments(self, request, queryset):
#         queryset.update(is_approved=False)

# # Selected Diplomas Inline for UserProfile
# class SelectedDiplomaInline(admin.TabularInline):
#     model = SelectedDiploma
#     extra = 0
#     verbose_name = "Selected Diploma"
#     verbose_name_plural = "Selected Diplomas"

# # User Profile Management
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'image', 'email')
#     search_fields = ('user__username', 'user__email')
#     ordering = ('user',)
#     inlines = [SelectedDiplomaInline]

#     def email(self, obj):
#         return obj.user.email if obj.user else "No email"

#     email.short_description = "Email"

# # Selected Diploma Management
# class SelectedDiplomaAdmin(admin.ModelAdmin):
#     list_display = ('user_profile', 'diploma', 'mode', 'level', 'taken_on')
#     list_filter = ('mode', 'level')
#     search_fields = ('user_profile__user__username', 'diploma__name')

# # Diploma Categories
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)

# # Payment Method Management
# class PaymentMethodAdmin(admin.ModelAdmin):
#     list_display = ('user', 'method_name')
#     search_fields = ('user__username', 'method_name')

# # Register the models and customize admin display
# admin.site.register(Diploma, DiplomaAdmin)
# admin.site.register(Comment, CommentAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(PaymentMethod, PaymentMethodAdmin)
# admin.site.register(SelectedDiploma, SelectedDiplomaAdmin)
# admin.site.site_header = "Diploma Management Admin"
# admin.site.site_title = "Diploma Admin Portal"
# admin.site.index_title = "Welcome to the Diploma Management Admin"





from django.contrib import admin
from .models import Diploma, UserProfile, Comment, Category, PaymentMethod, SelectedDiploma, Rating, Event, Module, Feedback, Subscription, Partner, Team, TrainingImage, ContactUs, GraduationImages, TrainingGallery
# from .forms import DiplomaAdminForm
from django.utils.html import format_html, format_html_join

# Sessions Admin Inline
# class SessionInline(admin.TabularInline):
#     model = Session
#     extra = 1
#     fields = ['title', 'content']
#     min_num = 1
#     verbose_name = "Session"
#     verbose_name_plural = "Sessions"


# Modules Admin Inline
class ModuleInline(admin.StackedInline): 
    model = Module
    extra = 1  # Number of empty module forms to display by default
    fields = ['title', 'duration', 'instructor', 'instructor_image', 'sessions', 'link', 'material_pdf', 'session_count']
    min_num = 1  # Minimum number of modules required
    verbose_name = "Module"
    verbose_name_plural = "Modules"
    # inlines = [SessionInline]
    readonly_fields = ['display_sub_content', 'session_count']

    def display_sub_content(self, obj):
        if obj.sub_content:
            bullet_points = format_html_join(
                '', "<li>{}</li>",
                ((line,) for line in obj.formatted_sub_content())
            )
            return format_html("<ul>{}</ul>", bullet_points)
        return "-"
    display_sub_content.short_description = "Sub Content (as bullet points)"

    def session_count(self, obj):
        return obj.session_count 
    session_count.short_description = "Session Count"

# Diploma Admin Panel
class DiplomaAdmin(admin.ModelAdmin):
#    form = DiplomaAdminForm
    list_display = ('name', 'category', 'price_egp', 'price_usd', 'start_course', 'end_course', 'link', 'module_count', 'total_sessions')
    # list_filter = ('category')
    search_fields = ('name', 'description')
    ordering = ('name',)
    inlines = [ModuleInline]

    # Automatically update module_count whenever the Diploma is saved
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_module_count()
        #obj.update_session_count()

    # To display total sessions
    def total_sessions(self, obj):
        
        return sum(module.session_count for module in obj.modules.all())
    total_sessions.short_description = "Total Sessions"

# Comments Management
class CommentAdmin(admin.ModelAdmin):
    list_display = ('diploma', 'user', 'content', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('content',)
    actions = ['approve_comments', 'reject_comments']

    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Reject selected comments')
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)
# Rating Management
class RatingAdmin(admin.ModelAdmin):
    list_display = ('diploma', 'user', 'score', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('user__username', 'diploma__name')
    actions = ['approve_ratings', 'reject_ratings']

    @admin.action(description='Approve selected ratings')
    def approve_ratings(self, request, queryset):
        queryset.update(is_approved=True)
        for rating in queryset:
            rating.diploma.update_rating()

    @admin.action(description='Reject selected ratings')
    def reject_ratings(self, request, queryset):
        queryset.update(is_approved=False)

# Wishlist Inline for UserProfile
class WishDiplomaInline(admin.TabularInline):
    model = UserProfile.wishlist.through 
    extra = 0
    verbose_name = "Wishlist Diploma"
    verbose_name_plural = "Wishlist Diplomas"
    can_delete = True

# Selected Diplomas Inline for UserProfile
class SelectedDiplomaInline(admin.TabularInline):
    model = SelectedDiploma
    extra = 0
    verbose_name = "Selected Diploma"
    verbose_name_plural = "Selected Diplomas"

# User Profile Management
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'image', 'email', 'phone_number', 'created_at')
    search_fields = ('user__username', 'email', 'full_name', 'phone_number')
    ordering = ('user',)
    inlines = [SelectedDiplomaInline, WishDiplomaInline]  

    def email(self, obj):
        return obj.user.email if obj.user else "No email"
    email.short_description = "Email"

    # Display the full name
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = "Full Name"

    # Display the username
    def username(self, obj):
        return obj.user.username if obj.user else "No username"
    username.short_description = "Username"

    # Display the account creation date
    def account_created(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else "No date"
    account_created.short_description = "Account Created"

    def wishlist_count(self, obj):
        return obj.wishlist.count()  # Assuming wishlist is a related_name in UserProfile

    wishlist_count.short_description = "Wishlist Count"

    # User Profile Management

class SelectedDiplomaAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'diploma',  'taken_on', 'is_approved')
    # list_filter = ('is_approved')
    search_fields = ('user_profile__user__username', 'diploma__name')
    @admin.action(description="Approve selected diplomas")
    def approve_diplomas(self, request, queryset):
        queryset.update(is_approved=True)

# Diploma Categories
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Payment Method Management
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'method_name')
    search_fields = ('user__username', 'method_name')

# Events Management
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'description')
    search_fields = ('title',)
    list_filter = ('date',)

# Feedback Managment
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'diploma', 'rating', 'comment', 'created_at')
    search_fields = ('name', 'diploma__name', 'comment')
# Subscription Managment
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at') 
    search_fields = ('email',)  
    list_filter = ('subscribed_at',)

# Team Managment
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    search_fields = ('name', )

# Training Inline for Partners
class TrainingImageInline(admin.TabularInline):
    model = TrainingImage
    extra = 1
    fields = ['image', 'title', 'description']

# Parteners Managment
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('company_name', )
    search_fields = ('name', )
    inlines = [TrainingImageInline]
# ContactUs Managment
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'diploma', 'created_at')
    search_fields = ('name', 'email', 'phone', 'question')
    list_filter = ('diploma', 'created_at')

class GraduationImagesAdmin(admin.ModelAdmin):
    list_display = ('name','image')

class TrainingGalleryAdmin(admin.ModelAdmin):
    list_display = ('name','image')

# Register the models
admin.site.register(Diploma, DiplomaAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(SelectedDiploma, SelectedDiplomaAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(GraduationImages, GraduationImagesAdmin)
admin.site.register(TrainingGallery, TrainingGalleryAdmin)
admin.site.site_header = "Land Mark Management Admin"
admin.site.site_title = "Land Mark Admin Portal"
admin.site.index_title = "Welcome to the Land Mark Management Admin"
