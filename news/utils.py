from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, get_connection, send_mail
from django.template.loader import render_to_string

# from environ import EMAIL_HOST_USER
import requests

import os


def get_filter_params(request):
    """Собирает параметры фильтрации постов"""

    temp = {p: v for p, v in request.GET.copy().items() if p != 'page'}
    if any([not not v for v in temp.values()]):
        return ''.join([f'&{p}={v}' for p, v in temp.items() if v])


def send_sub_emails(post):
    """Отправляет письмо всем подписчикам категории при создании поста в ней."""

    subscribers = User.objects.filter(categorysubscriber__category__in=post.category.all()).distinct()
    html_content = render_to_string(
        'news/email/new_post_email.html',
        {
            'title': post.title,
            'text': post.text,
            'id': post.id,
            'category': ', '.join(map(str, post.category.all())),
        }
    )
    emails = []
    for sub in subscribers:
        msg = EmailMultiAlternatives(
            subject=f'Здравствуйте, {sub}. Новая статья в твоём любимом разделе!',
            # from_email=EMAIL_HOST_USER,
            from_email=os.getenv('EMAIL_HOST_USER'),
            to=[sub.email],
        )

        msg.attach_alternative(html_content, "text/html")
        emails.append(msg)

    # Игнорируем ошибки, в частности - некорректные email-адреса.
    connection = get_connection(fail_silently=True)
    connection.send_messages(emails)


def send_contact_email(author, email, form):
    send_mail(
        f'[NewsPaperProject] New message from {author}',
        f'Subject: {form.cleaned_data["title"]}\n\n{form.cleaned_data["text"]}\n\nUser email: {email}',
        EMAIL,
        [EMAIL],
        fail_silently=False
    )


class Attitude:
    """Миксин-класс для моделей с полем rating"""

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


def is_url_valid(url):
    response = requests.get(url)
    if response.status_code == 404:
        return False
    else:
        return True
