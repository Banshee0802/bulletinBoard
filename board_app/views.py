from django.shortcuts import render, redirect, get_object_or_404
from .models import Advertisement, Request, Category
from .forms import AdvertisementForm
from django.contrib.auth.decorators import login_required

def main_page(request):
    return render(request, 'board/main_page.html')


def ad_list(request):
    ads = Advertisement.objects.all().order_by('-created_at')
    return render(request, 'board/ad_list.html', context={'ads': ads})


def ad_detail(request, id):
    advertisement = get_object_or_404(Advertisement, id=id)

    has_requested = False
    if request.user.is_authenticated:
        has_requested = Request.objects.filter(
            advertisement=advertisement,
            sender=request.user
        ).exists()

    return render(request, 'board/ad_detail.html', context={'advertisement': advertisement, 'has_requested': has_requested})


@login_required
def ad_edit(request, id):
    title = "Редактировать объявление"
    submit_button_text = 'Обновить'
    advertisement = get_object_or_404(Advertisement, id=id)

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)

        if form.is_valid():
            edit_ad = form.save()

            return redirect('ad_detail', id=edit_ad.id)
        else:
            return render(request, 'board/ad_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})
        
    form = AdvertisementForm(instance=advertisement)

    return render(request, 'board/ad_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})


@login_required
def ad_delete(request, slug):
    advertisement = get_object_or_404(Advertisement, slug=slug)

    if request.method == 'POST':
        advertisement.delete()

        return redirect('ad_list')
    return render(request, 'board/confirm_ad_delete.html', {'advertisement': advertisement})

@login_required
def ad_create(request):
    title = 'Создать объявление'
    submit_button_text = 'Опубликовать'

    if request.method == 'GET':
        form = AdvertisementForm()

        return render(request, 'board/ad_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})
    
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)

        if form.is_valid():
            advertisement = form.save(commit=False)

            advertisement.user = request.user

            advertisement.save()

            return redirect('ad_detail', id=advertisement.id)
        else:
            return render(request, 'board/ad_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})
        

@login_required
def send_request(request, id):
    advertisement = get_object_or_404(Advertisement, id=id)

    if advertisement.user == request.user:
        return redirect('ad_detail', id=id)
    
    existing_request = Request.objects.filter(sender=request.user, advertisement=advertisement).first()
    if existing_request:
        return redirect('ad_detail', id=id)
    
    new_request = Request.objects.create(
        sender=request.user,
        receiver=advertisement.user,
        advertisement=advertisement,
        status='new',
    )
    return redirect('ad_detail', id=id)
    

def ads_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    ads = Advertisement.objects.filter(category=category)
    
    return render(request, 'board/ad_list.html', {'category': category, 'ads': ads})


def category_list(request):
    categories = Category.objects.all()
    
    return render(request, 'board/category_list.html', {'categories': categories})