from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('ads/', views.ad_list, name='ad_list'),
    path('ad/<int:id>/', views.ad_detail, name='ad_detail'),
    path('ad/<int:id>/edit/', views.ad_edit, name='ad_edit'),
    path('ad/<int:id>/delete/', views.ad_delete, name='ad_delete'),
    path('ad/create/', views.ad_create, name='ad_create'),
]
