# RSS для статей
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

# Feed – класс подсистемы фидов Django. Атрибуты  title,  link и description  
# будут представлены  в RSS элементами <title>, <link> и <description>
class LatestPostsFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    # получает объекты, которые будут включены в рассылку. Мы берем только 
    # последние 5 опубликованных статей для этого фида
    def items(self):
        return Post.published.all()[:5]

    # получает для каждого объекта из результата items() заголовок и описание
    def item_title(self, item):
        return item.title

    # Получает для каждого объекта из результата items() заголовок и описание.
    # Встроенный шаблонный фильтр truncatewords, чтобы ограничить описание 
    # статей тридцатью словами.
    def item_description(self, item):
        return truncatewords(item.body, 30)
