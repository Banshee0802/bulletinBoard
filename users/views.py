from django.views import View
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, get_user_model, authenticate
from .forms import RegisterForm, LoginForm
from board_app.models import Advertisement, Request
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from config.settings import LOGIN_REDIRECT_URL, DEFAULT_FROM_EMAIL

User = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        self.send_activation_email(user)

        messages.success(
            self.request, 
            'Регистрация прошла успешно! Проверьте почту для активации аккаунта'
            )

        return redirect('login')
    
    def send_activation_email(self, user):
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = self.request.build_absolute_uri(reverse_lazy('activate_account', kwargs={'uidb64': uidb64, 'token': token}))

        site_name = get_current_site(self.request).name
        
        subject = render_to_string('users/emails/subjects/activate_account.txt', {
            'site_name': site_name,
        })
        message = render_to_string('users/emails/activate_account.txt', {
            'site_name': site_name,
            'activation_url': activation_url
        })
        html_message = render_to_string('users/emails/activate_account.html', {
            'site_name': site_name,
            'activation_url': activation_url
        })
        

        send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Аккаунт успешно активирован! Войдите в аккаунт')
            return redirect('login')
        else:
            messages.error(request, 'Ссылка активации недействительна или устарела')
            return redirect('register')

    
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
    

@require_POST
def change_theme(request):
    theme = request.POST.get('theme', 'light')
    request.session['theme'] = theme
    return redirect(request.META.get('HTTP_REFERER', '/'))


class CustomPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('password_change_done')
    success_message = "Пароль успешно изменен!"

class CustomPasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'users/password_change_done.html'