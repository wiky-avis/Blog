from django.shortcuts import render, get_object_or_404
from .models import Post

# обработчик для отображения списка статей
def post_list(request):
    posts = Post.published.all() # одно и то же, что и Post.objects.all()
    return render(request, 'blog/post/list.html', {'posts': posts})
