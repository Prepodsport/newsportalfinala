# from allauth.account.signals import email_confirmed, user_signed_up
# from django.core.mail import EmailMultiAlternatives, send_mail
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from django.template.loader import render_to_string
# from django.conf import settings
# from .models import PostCategory
#
#
# def send_notifications(preview, pk, title, subscribers):
#     html_content = render_to_string(
#         'news_pages/post_created_email.html',
#         {
#             'text': preview,
#             'link': f'{settings.SITE_URL}/news/{pk}'
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.post_category.all()
#         subscribers: list[str] = []
#         for category in categories:
#             subscribers += category.subscribers.all()
#
#         subscribers = [s.email for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.title, subscribers)
#
#
# @receiver(email_confirmed)
# def user_signed_up(request, email_address, **kwargs):
#     # отправляется письмо пользователю, чья почта была подтверждена
#     send_mail(
#         subject=f'Привет {email_address.user} Добро пожаловать на News Portal!',
#         message=f'Приветствую Вас на моём новостном портале. Здесь самые последние новости из разных категорий',
#         from_email='NewsPortalDjango@yandex.ru',
#         recipient_list=[email_address.user.email]
#     )
