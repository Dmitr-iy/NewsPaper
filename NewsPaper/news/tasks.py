import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category


@shared_task
def send_message(oid):
    post = Post.objects.get(pk=oid)
    categories = post.category.all()
    for item in categories:
        for s in item.subscribers.all():
            html_content = render_to_string(
                'post_created_email.html',
                {
                    'text': post.text,
                    'link': f'{settings.SITE_URL}/news/{post.pk}',
                }
            )

            msg = EmailMultiAlternatives(
                subject=post.title,
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[s.email],
            )

            msg.attach_alternative(html_content, 'text/html')
            msg.send()


@shared_task
def every_week_message():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateTime__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Articles for the week',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
