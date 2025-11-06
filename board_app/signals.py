from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from config.settings import DEFAULT_FROM_EMAIL, SITE_URL
from .models import News

User = get_user_model()

@receiver(post_save, sender=News)
def email_important_news_notifications(sender, instance, created, **kwargs):
    if created and instance.is_important:
        active_users = User.objects.filter(is_active=True)
        subscribers = active_users

        for user in subscribers:
            subject = f'Важная новость: {instance.advertisement.title}'

            html_message = render_to_string('board/emails/important_news_notification.html', {
                'news': instance,
                'site_url': SITE_URL
            })

            send_mail(
                subject=subject,
                message='',
                html_message=html_message,
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[user.email]
            )