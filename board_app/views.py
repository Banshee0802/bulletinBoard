from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Advertisement, Request, Category, Tag
from .forms import AdvertisementForm, TagForm

class MainPageView(TemplateView):
    template_name = 'board/main_page.html'

class AdListView(ListView):
    model = Advertisement
    template_name = 'board/ad_list.html'
    context_object_name = 'ads'
    ordering = ['-created_at']

class AdDetailView(DetailView):
    model = Advertisement
    template_name = 'board/ad_detail.html'
    context_object_name = 'advertisement'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advertisement = self.get_object()
        
        has_requested = False
        if self.request.user.is_authenticated:
            has_requested = Request.objects.filter(
                advertisement=advertisement,
                sender=self.request.user
            ).exists()
        
        context['has_requested'] = has_requested
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
        return response
    
    def form_invalid(self, form):
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
        return response
    
    def form_invalid(self, form):
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
    template_name = 'board/ad_list.html'
    context_object_name = 'ads'
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Advertisement.objects.filter(category=self.category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'board/category_list.html'
    context_object_name = 'categories'

class AdsByTagView(ListView):
    template_name = 'board/ads_by_tag.html'
    context_object_name = 'ads'
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Advertisement.objects.filter(tags=self.tag).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['title'] = f'Объявления с тегом "{self.tag.name}"'
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


    