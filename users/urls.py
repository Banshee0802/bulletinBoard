from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<str:user_name>/', views.profile_view, name='profile'),
    path('request/<int:request_id>/update_status/', views.request_update_status, name='request_update_status')
]
