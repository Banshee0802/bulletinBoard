from django.shortcuts import render, redirect, get_object_or_404
from .models import Advertisement
from .forms import AdvertisementForm
from django.contrib.auth.decorators import login_required

def main_page(request):
    return render(request, 'board/main_page.html')


def ad_list(request):
    ads = Advertisement.objects.all().order_by('-created_at')
    return render(request, 'board/ad_list.html', context={'ads': ads})


def ad_detail(request, id):
    advertisement = get_object_or_404(Advertisement, id=id)
    return render(request, 'board/ad_detail.html', context={'advertisement': advertisement})


@login_required
def ad_edit(request, id):
    title = "Редактировать объявление"
    submit_button_text = 'Обновить'
    advertisement = get_object_or_404(Advertisement, id=id)

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=advertisement)

        if form.is_valid():
            edit_ad = form.save()

            return redirect('ad_detail', id=edit_ad.id)
        else:
            return render(request, 'board/ad_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})
        
    form = AdvertisementForm(instance=advertisement)

    return render(request, 'board/ad_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})


@login_required
def ad_delete(request, id):
    advertisement = get_object_or_404(Advertisement, id=id)

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
        form = AdvertisementForm(request.POST)

        if form.is_valid():
            advertisement = form.save(commit=False)

            advertisement.user = request.user

            advertisement.save()

            return redirect('ad_detail', id=advertisement.id)
        else:
            return render(request, 'board/ad_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})
    