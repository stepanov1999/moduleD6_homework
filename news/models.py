from django.db.models import Sum
from django.urls import reverse_lazy
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache

from .utils import Attitude


class Author(models.Model):
    author_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.author_user.get_username()

    def update_rating(self):
        posts_rating = self.post_set.all().aggregate(posts_rating=Sum('rating'))
        p_r = posts_rating.get('posts_rating', 0) * 3

        comments_ratings = self.author_user.comment_set.all().aggregate(c_rating=Sum('rating'))
        c_r = comments_ratings.get('c_rating', 0)
        self.rating = p_r + c_r
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscriber')

    def __str__(self):
        return self.name

    def subscribe(self):
        return reverse_lazy('subscribe', kwargs={'pk': self.id})

    def unsubscribe(self):
        return reverse_lazy('unsubscribe', kwargs={'pk': self.id})


class Post(models.Model, Attitude):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1,
                            choices=[('N', 'News'), ('A', 'Article')],
                            default='A')
    publish_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=150)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    voted = models.ManyToManyField(User, through='PostVote')

    def preview(self):
        return f'{self.text[:124]}...'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('post', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        cache.delete(f'post_{self.pk}')
        cache.delete('posts_list')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cache.delete(f'post_{self.pk}')
        cache.delete('posts_list')
        super().delete(*args, **kwargs)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class CategorySubscriber(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model, Attitude):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    publish_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    def get_delete_url(self):
        return reverse_lazy('delete_comment', kwargs={'pk': self.pk})


class PostVote(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'post_id')

    def __str__(self):
        return f'{self.user_id} - {self.post_id}'


class SubscribedUsersCategory(models.Model):
    subscribed_users = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
