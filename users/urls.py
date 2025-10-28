from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import ( 
    RegisterView, CustomLoginView, CustomLogoutView, 
    ProfileView, RequestUpdateStatusView, change_theme, 
    CustomPasswordChangeView, CustomPasswordChangeDoneView,
    ActivateAccountView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('activate-account/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate_account'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/<str:user_name>/', ProfileView.as_view(), name='profile'),
    path('request/<int:request_id>/update_status/', RequestUpdateStatusView.as_view(), name='request_update_status'),
    path('change_theme/', change_theme, name='change_theme'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/emails/password_reset_email.html',
        subject_template_name='users/emails/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done'),
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),
    
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html',
    ), name='password_reset_complete'),
]
