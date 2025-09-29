from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, get_user_model, authenticate
from .forms import RegisterForm, LoginForm
from board_app.models import Advertisement, Request
from django.contrib import messages


User = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('ad_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Регистрация прошла успешно!')
        
        return response
        
    
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    
    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        
        if next_url and not 'login' in next_url:
            return next_url
        return reverse_lazy('ad_list') 
    
    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно вошли!')
        return super().form_valid(form)
        
    def form_invalid(self, form):
        messages.error(self.request, 'Неверный логин или пароль')
        return super().form_invalid(form)  
    

class CustomLogoutView(LogoutView):
    next_page = 'ad_list'
    

class ProfileView(TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.kwargs.get('user_name')
        user = get_object_or_404(User, username=user_name)

        context['user'] = user
        context['ads'] = Advertisement.objects.filter(user=user).order_by('-created_at')
        context['requests'] = Request.objects.filter(receiver=user).order_by('-created_at')
        return context
        

class RequestUpdateStatusView(LoginRequiredMixin, View):

    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        request_id = self.kwargs.get('request_id')
        req = get_object_or_404(Request, id=request_id)

        if req.receiver != self.request.user:
            return redirect('profile', user_name=self.request.user.username)
        
        new_status = self.request.POST.get('status')
        if new_status in ['accepted', 'rejected']:
            req.status = new_status
            req.save()

        return redirect('profile', user_name=self.request.user.username)