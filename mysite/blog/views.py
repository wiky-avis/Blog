from django.shortcuts import render, get_object_or_404
from .models import Post
# пагинатор
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# обработчик для отображения списка статей
def post_list(request):
    posts = Post.published.all() # одно и то же, что и Post.objects.all()
    # добавляем пагинатор
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # По 3 статьи на каждой странице.
    page = request.GET.get('page') #  извлекаем  из  запроса  GET-параметр  
    # page,  который  указывает  текущую страницу
    try:
        posts = paginator.page(page) # получаем список объектов на нужной 
        # странице с помощью метода page() класса Paginator
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, 
        # возвращаем последнюю.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})  
    # передаем номер страницы и полученные объекты в шаблон.
    # функция render() для  формирования HTML-шаблона

# обработчик  для  отображения  статьи
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, slug=post, status='published', publish__year=year, 
        publish__month=month, publish__day=day
        ) # Если объекта не существует, будет поднята ошибка 404
    return render(request, 'blog/post/detail.html', {'post': post})

