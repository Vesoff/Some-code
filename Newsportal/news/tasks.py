import datetime

from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Post, Category


@shared_task
def weekly_send_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)
    category = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=category).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_email_notification(pk):
    posts = Post.objects.filter(pk=pk)
    category = set(posts.values_list('category__name', flat=True))
    title = posts.title
    subscribers_emails = []

    for cat in category:
        subscribers = cat.subscribers.all()
        subscribers_emails += [s.email for s in subscribers]

    html_content = render_to_string(
        'mail/post_created_email.html',
        {
            'text': posts.preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
