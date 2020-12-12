# карта сайта
from django.contrib.sitemaps import Sitemap
from .models import Post

# создаем собственный объект карты сайта, унаследовав его от Sitemap
class PostSitemap(Sitemap):
    # changefreq и priority показывают частоту обновления страниц статей
    changefreq = 'weekly'
    priority = 0.9

    # возвращает QuerySet объектов, которые будут отображаться в карте сайта
    def items(self):
        return Post.published.all()

    # lastmod принимает каждый объект из результата вызова items() и возвращает 
    # время последней модификации статьи
    def lastmod(self, obj):
        return obj.updated