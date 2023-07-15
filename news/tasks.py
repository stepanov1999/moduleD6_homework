from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import User, Post
import os


def my_job():
    subscribers = User.objects.filter(categorysubscriber__isnull=False).distinct()
    emails = []
    print(subscribers)
    for sub in subscribers:
        last_week = timezone.now() - timedelta(days=7)

        posts_to_notify = Post.objects.filter(
            Q(category__categorysubscriber__subscriber=sub)
            & Q(publish_time__gte=last_week)).distinct()

        if posts_to_notify:
            html_content = render_to_string(
                'news/email/notify_weekly.html',
                {
                    'posts': posts_to_notify,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'Здравствуйте, {sub}. Предлагаем список новых статей за неделю '
                        f'в категориях, на которые вы подписаны.',
                from_email=os.getenv('EMAIL_HOST_USER'),
                to=[sub.email],
            )

            msg.attach_alternative(html_content, "text/html")
            emails.append(msg)

    connection = get_connection(fail_silently=True)
    connection.send_messages(emails)
