from celery import shared_task
import time
# import redis

# red = redis.Redis(
#     host='redis-11875.c266.us-east-1-3.ec2.cloud.redislabs.com',
#     port=11875,
#     password='hBJDaMbZdc6dHEKabxg5V2TKDyP3ZWBn'
# )
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
import datetime
from allauth.account.signals import email_confirmed, user_signed_up
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from .models import PostCategory


@shared_task
def send_notifications(preview, pk, title, subscribers, sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)
    html_content = render_to_string(
        'news_pages/post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i + 1)


@shared_task
def notify_email_weeks():
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_created__gte=last_week)
    categories = set(posts.values_list("post_category__article_category", flat=True))
    subscribers = set(
        Category.objects.filter(article_category__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'week_notify.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email="NewsPortalDjango@yandex.ru",
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def user_signed_up(request, email_address, **kwargs):
    # отправляется письмо пользователю, чья почта была подтверждена
    send_mail(
        subject=f'Привет {email_address.user} Добро пожаловать на News Portal!',
        message=f'Приветствую Вас на моём новостном портале. Здесь самые последние новости из разных категорий',
        from_email='NewsPortalDjango@yandex.ru',
        recipient_list=[email_address.user.email]
    )
