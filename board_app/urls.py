from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('ads/', views.AdListView.as_view(), name='ad_list'),
    path('ad/<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('ad/<int:pk>/edit/', views.AdUpdateView.as_view(), name='ad_edit'),
    path('ad/<slug:slug>/delete/', views.AdDeleteView.as_view(), name='ad_delete'),
    path('ad/create/', views.AdCreateView.as_view(), name='ad_create'),
    path('ad/<int:pk>/send_request/', views.SendRequestView.as_view(), name='send_request'),
    path('ads/tag/<slug:tag_slug>/', views.AdsByTagView.as_view(), name='ads_by_tag'),
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/add/', views.AddTagView.as_view(), name='add_tag'),
    path('ads/category/<slug:category_slug>/', views.AdsByCategoryView.as_view(), name='ads_by_category'),
    path('ads/categories/', views.CategoryListView.as_view(), name='ad_categories'),
    path('ads/admin-ads/', views.AdminAdsView.as_view(), name='admin_ads'),
    path('toggle-favorite/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
]