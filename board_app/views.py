from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Advertisement, Request, Category, Tag
from .forms import AdvertisementForm, TagForm
from django.db.models import F
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
import json
import time
from django.contrib import messages
from django.template.loader import render_to_string

class MainPageView(TemplateView):
    template_name = 'board/main_page.html'


class AdSearchView(ListView):
    model = Advertisement
    template_name = 'board/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 6

    def get_queryset(self):
        queryset = Advertisement.objects.all().order_by('-created_at')
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')
        context['search_query'] = search_query
        context['is_search'] = bool(search_query)
        return context


class AdListView(ListView):
    model = Advertisement
    template_name = 'board/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 6 

    def get_queryset(self):
        return Advertisement.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_search'] = False
        context['search_query'] = ''
        context['has_more'] = self.get_queryset().count() > self.paginate_by

        return context
    

class LoadMoreAdsView(View):
    def get(self, request):
        time.sleep(1) 

        offset = int(request.GET.get('offset'))
        paginate_by = 6
        ads_queryset = Advertisement.objects.all().order_by('-created_at')
        ads = ads_queryset[offset:offset + paginate_by]

        html = ''.join([
            render_to_string('board/includes/ads_container_include.html', {'advertisement': ad, 'request': request}, request)
            for ad in ads
        ])

        has_more = offset + paginate_by < ads_queryset.count()

        return JsonResponse({
            'html': html,
            'has_more': has_more,
        })


class AdDetailView(DetailView):
    model = Advertisement
    template_name = 'board/ad_detail.html'
    context_object_name = 'advertisement'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user != self.object.user:
            Advertisement.objects.filter(pk=self.object.pk).update(views=F('views') + 1)

            self.object.refresh_from_db()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advertisement = self.get_object()
        
        has_requested = False
        is_favorite = False

        if self.request.user.is_authenticated:
            has_requested = Request.objects.filter(
                advertisement=advertisement,
                sender=self.request.user
            ).exists()
            
            is_favorite = self.request.user in advertisement.favorites.all()
        
        context['has_requested'] = has_requested
        context['is_favorite'] = is_favorite
        return context

class AdCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'board/ad_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать объявление'
        context['submit_button_text'] = 'Опубликовать'
        context['current_tags'] = None
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        form.save_m2m()
        messages.success(self.request, 'Пост успешно создан!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании поста')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('ad_detail', kwargs={'pk': self.object.id})

class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'board/ad_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать объявление'
        context['submit_button_text'] = 'Обновить'
        context['current_tags'] = self.object.tags.all()
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        form.save_m2m()
        messages.success(self.request, 'Пост успешно обновлен!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при редактировании поста')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('ad_detail', kwargs={'pk': self.object.id})

class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Advertisement
    template_name = 'board/confirm_ad_delete.html'
    success_url = reverse_lazy('ad_list')
    
    def get_object(self, queryset=None):
        return get_object_or_404(Advertisement, slug=self.kwargs['slug'])

class SendRequestView(LoginRequiredMixin, DetailView):
    model = Advertisement
    http_method_names = ['post'] 
    
    def post(self, request, *args, **kwargs):
        advertisement = self.get_object()
        
        if advertisement.user == request.user:
            return redirect('ad_detail', pk=advertisement.id)
        
        existing_request = Request.objects.filter(
            sender=request.user, 
            advertisement=advertisement
        ).first()
        
        if existing_request:
            return redirect('ad_detail', pk=advertisement.id)
        
        Request.objects.create(
            sender=request.user,
            receiver=advertisement.user,
            advertisement=advertisement,
            status='new',
        )
        
        return redirect('ad_detail', pk=advertisement.id)

class AdsByCategoryView(ListView):
    model = Advertisement
    template_name = 'board/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 6

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Advertisement.objects.filter(category=category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context['is_search'] = False
        context['search_query'] = ''
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'board/category_list.html'
    context_object_name = 'categories'

class AdsByTagView(ListView):
    model = Advertisement
    template_name = 'board/ads_by_tag.html'
    context_object_name = 'ads'
    paginate_by = 6

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Advertisement.objects.filter(tags=tag).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        context['title'] = f'Объявления с тегом "{context["tag"].name}"'
        context['is_search'] = False
        context['search_query'] = ''
        return context


class AddTagView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'board/add_tag.html'
    success_url = reverse_lazy('tag_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать новый тег'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Тег успешно создан!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании тега')
        return super().form_invalid(form)

class TagListView(ListView):
    model = Tag
    template_name = 'board/tag_list.html'
    context_object_name = 'tags'
    ordering = ['name']


class AdminAdsView(ListView):
    model = Advertisement
    template_name = 'board/admin_ads.html'
    context_object_name = 'ads'
    paginate_by = 6

    def get_queryset(self):
        return Advertisement.objects.filter(user__is_superuser=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_search'] = False
        context['search_query'] = ''
        return context
    

class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        advertisement_id = request.POST.get('advertisement_id')
        advertisement = get_object_or_404(Advertisement, pk=advertisement_id)
        
        if request.user in advertisement.favorites.all():
            advertisement.favorites.remove(request.user)
            is_favorite = False
        else:
            advertisement.favorites.add(request.user)
            is_favorite = True

        return JsonResponse({
            'is_favorite': is_favorite,
            'favorites_count': advertisement.favorites.count()
        })
        

class FavoriteListView(ListView):
    model = Advertisement
    template_name = 'board/favorite_ads.html'
    context_object_name = 'ads'
    paginate_by = 3

    def get_queryset(self):
        return self.request.user.favorite_ads.all().order_by('-created_at')
    
        