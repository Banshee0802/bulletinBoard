from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView, ProfileView, RequestUpdateStatusView, change_theme

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/<str:user_name>/', ProfileView.as_view(), name='profile'),
    path('request/<int:request_id>/update_status/', RequestUpdateStatusView.as_view(), name='request_update_status'),
    path('change_theme/', change_theme, name='change_theme'),
]
