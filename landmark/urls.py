from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('', views.contact_us_view, name='contact_us'),
    path('minimba', views.mini_mba, name='mini_mba'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/',views.logout_view, name="logout"),
    path('profile/', views.user_profile, name='profile'),
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('diplomas/', views.diploma_list, name='diploma_list'),
    path('diplomas/enroll/<int:diploma_id>/', views.enroll_diploma, name='enroll_diploma'),
    # path('mini-mba/enroll/<int:diploma_id>/', views.enroll_diploma, name='enroll_mini_mba'),
    path('minimba/enroll/<int:diploma_id>/', views.enroll_minimba, name='enroll_mba'),
    # path('diplomas/<int:diploma_id>/', views.diploma_detail, name='diploma_detail'),
    # path('diplomas/<int:diploma_id>/take/', views.take_diploma, name='take_diploma'),
    # path('wishlist/add/<int:diploma_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    # path('wishlist/remove/<int:diploma_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('feedback/', views.feedback_view, name='feedback'),
    # path('thank-you/', views.thank_you, name='thank_you'),
    path('api/subscribe/', views.subscribe, name='subscribe'),
    # path('verify-email/', views.verify_email, name='verify_email'),
    path('about/',views.about, name='about'),
    path('training/',views.training, name='training'),
    path('consulting/',views.consulting, name='consulting'),
    path('assesment/',views.assesment, name='assesment')
]
