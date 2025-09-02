from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('ads/', views.ad_list, name='ad_list'),
    path('ad/<int:id>/', views.ad_detail, name='ad_detail'),
    path('ad/<int:id>/edit/', views.ad_edit, name='ad_edit'),
    path('ad/<slug:slug>/delete/', views.ad_delete, name='ad_delete'),
    path('ad/create/', views.ad_create, name='ad_create'),
    path('ad/<int:id>send_request/', views.send_request, name='send_request'),
    path('ads/tag/<slug:tag_slug>/', views.ads_by_tag, name='ads_by_tag'),
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/add/', views.add_tag, name='add_tag'),
    path('ads/category/<slug:category_slug>/', views.ads_by_category, name='ads_by_category'),
    path('ads/categories/', views.category_list, name='ad_categories'),
]
