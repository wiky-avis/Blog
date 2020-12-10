from django.shortcuts import render, get_object_or_404
from .models import Post

# обработчик для отображения списка статей
def post_list(request):
    posts = Post.published.all() # одно и то же, что и Post.objects.all()
    return render(request, 'blog/post/list.html', {'posts': posts}) 
    # функция render() для  формирования HTML-шаблона

# обработчик  для  отображения  статьи
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, slug=post, status='published', publish__year=year, 
        publish__month=month, publish__day=day
        ) # Если объекта не существует, будет поднята ошибка 404
    return render(request, 'blog/post/detail.html', {'post': post})

