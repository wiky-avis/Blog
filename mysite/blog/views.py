from django.shortcuts import render, get_object_or_404
from .models import Post
# пагинатор
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# ListView базовый класс обработчика списков позволяет отображать несколько 
# объектов любого типа.
from django.views.generic import ListView

# вместо этой функции написали class PostListView, который намного меньше по 
# объему кода
# # обработчик для отображения списка статей
# def post_list(request):
#     posts = Post.published.all() # одно и то же, что и Post.objects.all()
#     # добавляем пагинатор
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 3) # По 3 статьи на каждой странице.
#     page = request.GET.get('page') #  извлекаем  из  запроса  GET-параметр  
#     # page,  который  указывает  текущую страницу
#     try:
#         posts = paginator.page(page) # получаем список объектов на нужной 
#         # странице с помощью метода page() класса Paginator
#     except PageNotAnInteger:
#         # Если страница не является целым числом, возвращаем первую страницу.
#         posts = paginator.page(1)
#     except EmptyPage:
#         # Если номер страницы больше, чем общее количество страниц, 
#         # возвращаем последнюю.
#         posts = paginator.page(paginator.num_pages)
#     return render(
#         request, 'blog/post/list.html', {'page': page, 'posts': posts})  
#     # передаем номер страницы и полученные объекты в шаблон.
#     # функция render() для  формирования HTML-шаблона

# обработчик  для  отображения  статьи
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, slug=post, status='published', publish__year=year, 
        publish__month=month, publish__day=day
        ) # Если объекта не существует, будет поднята ошибка 404
    return render(request, 'blog/post/detail.html', {'post': post})


# вместо обработчика post_list
class PostListView(ListView):
    #переопределенный  QuerySet  модели  вместо  получения всех объектов
    queryset = Post.published.all()
    #  posts  в  качестве  переменной  контекста  HTML-шаблона, в которой будет 
    # храниться список объектов. Если не указать атрибут con-text_object_name, 
    # по умолчанию используется переменная object_list;
    context_object_name= 'posts'
    # постраничное отображение по три объекта на странице;
    paginate_by = 3
    # шаблон для формирования страницы. Если бы мы не указали template_name, 
    # то базовый класс ListView использовал бы шаблон blog/post_list.html.
    template_name = 'blog/post/list.html'

