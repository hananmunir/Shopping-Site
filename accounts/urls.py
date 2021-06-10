from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='login'),
    path('our_policies/', policies_view, name='Policy'),
    path('signup/', signup_view, name='signup'),
    path('accounts/', accounts_view,name = 'accounts'),
    path('accounts/update_personal_info', personal_info_update_view,name = 'personal-info-update'),
    path('accounts/update_address', address_update_view,name = 'address-update'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name = "password_change.html"), name = 'reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name ="password_reset_email_sent.html" ), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name ="password_reset_form.html"), name = 'password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = "password_change_successful.html"), name = 'password_reset_complete')
]