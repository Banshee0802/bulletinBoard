from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from .forms import RegisterForm, LoginForm
from django.conf import settings
from board_app.models import Advertisement


User = get_user_model()


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ad_list')

    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})  


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get('next') or settings.LOGIN_REDIRECT_URL
            return redirect(next_url)
        
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})
    

def logout_view(request):
    logout(request)
    return redirect('ad_list')


def profile_view(request, user_name):
    user = get_object_or_404(User, username=user_name)

    ads = Advertisement.objects.filter(user=user).order_by('-created_at')

    context = {
        'user': user,
        'ads': ads
    }

    return render(request, 'users/profile.html', context)

