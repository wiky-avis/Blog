# Создание собственных тегов
from django import template
from ..models import Post
from django.db.models import Count
# Создание собственных фильтров
from django.utils.safestring import mark_safe
# нужно установить pip install Markdown
import markdown


register = template.Library()

# выводит количество опубликованных  статей
# Django будет использовать название функции в качестве названия тега.
# Можно указать явно, как обращаться к тегу из шаблонов 
# – @register.simple_tag(name='my_tag').
@register.simple_tag  # декоратор для регистрации нового тега
def total_posts():
    return Post.published.count()


# Тег для добавления последних статей блога на боковую панель.
# Мы будем использовать инклюзивный тег, с помощью которого сможем 
# задействовать переменные контекста, возвращаемые тегом, для формирования 
# шаблона.
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# Шаблонный тег для отображения статей с наибольшим количеством комментариев
# Мы формируем QuerySet, используя метод annotate() для добавления к каждой 
# статье количества ее комментариев. Count используется в качестве функции 
# агрегации, которая вычисляет количество комментариев total_comments для 
# каждого объекта Post.
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
        ).order_by('-total_comments')[:count]


# добавляет возможность заполнять тело статьи с помощью форматирования Markdown, которое 
# будет формировать корректный HTML при отображении статьи.
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))