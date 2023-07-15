from django.core.exceptions import PermissionDenied
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.utils import timezone

from news.models import Post
from news.utils import send_sub_emails


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        send_sub_emails(instance)


@receiver(pre_save, sender=Post)
def limit_posts_per_day(sender, instance, **kwargs):
    author = instance.author
    posts_today = Post.objects.filter(
        author=author, publish_time__date=timezone.now().date()
    ).count()
    if posts_today >= 3:
        raise PermissionDenied('Превышен лимит на количество постов в день.<br>'
                               'Попробуйте опубликовать новый пост завтра или удалите '
                               'один из трех предыдущих постов<br><br>'
                               f'Заголовок: {instance.title}<br>Текст:<br>{instance.text}')
