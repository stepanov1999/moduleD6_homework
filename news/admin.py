from django.contrib import admin
from .models import Author, Comment, Post, Category, PostVote


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'post_categories', 'type', 'publish_time')
    list_filter = ('author', 'category')
    search_fields = ('author', 'category')

    @staticmethod
    def post_categories(obj):
        return ', '.join([str(cat) for cat in obj.category.all()])


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'all_subscribers', 'all_posts')
    search_fields = ('name', 'all_subscribers', 'all_posts')

    @staticmethod
    def all_subscribers(obj):
        return ', '.join([str(sub) for sub in obj.subscribers.all()])

    @staticmethod
    def all_posts(obj):
        return ', '.join([str(post) for post in Post.objects.filter(category=obj)])


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_user', 'posts')

    @staticmethod
    def posts(obj):
        return ' | '.join([str(post) for post in Post.objects.filter(author=obj)])


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'text', 'publish_time')
    list_filter = ('publish_time',)
    search_fields = ('post', 'user')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostVote)
