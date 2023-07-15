from django import template


register = template.Library()


@register.filter(name='censor')
def censor(value):
    banned_words = ['черт', 'блять', 'сука', 'хуй']
    original_text = value.split()

    bad_words = []
    for indx, word in enumerate(value.lower().split()):
        for bad_word in banned_words:
            if bad_word in word:
                bad_words.append(indx)
    for bad_word in bad_words:
        original_text[bad_word] = '*нехорошее слово*'

    return ' '.join(original_text)


@register.filter(name="is_author")
def has_group(user):
    return user.groups.filter(name='authors').exists()


@register.filter(name="is_post_author")
def is_post_author(user, post):
    return user == post.author.author_user
