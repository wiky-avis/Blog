from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
# пагинатор
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# ListView базовый класс обработчика списков позволяет отображать несколько 
# объектов любого типа.
from django.views.generic import ListView
# форма для отправки писем
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
# теги
from taggit.models import Tag



# обработчик для отображения списка статей
def post_list(request, tag_slug=None):
    posts = Post.published.all() # одно и то же, что и Post.objects.all()
    # добавляем пагинатор
    object_list = Post.published.all()

    #  возможность фильтровать список статей по определенному тегу
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    
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
    return render(
        request, 'blog/post/list.html', 
        {'page': page, 'posts': posts, 'tag': tag}
        )  
    # передаем номер страницы и полученные объекты в шаблон.
    # функция render() для  формирования HTML-шаблона

# обработчик  для  отображения  статьи
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, slug=post, status='published', publish__year=year, 
        publish__month=month, publish__day=day
        ) # Если объекта не существует, будет поднята ошибка 404

    # добавляем комментарии на страницу
    # Список активных комментариев для этой статьи.
    # Мы создали объект QuerySet, используя объект статьи post и менеджер 
    # связанных объектов comments, определенный в модели Comment в аргументе 
    # related_name.
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # Bнициализация формы при GET-запросе.Пользователь отправил комментарий.
        comment_form = CommentForm(data=request.POST)
        # Если же получаем POST-запрос, то заполняем форму данными из запроса 
        # и валидируем ее методом is_valid()
        if comment_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в базе данных.
            new_comment = comment_form.save(commit=False)
            # Привязываем комментарий к текущей статье.
            new_comment.post = post
            # Сохраняем комментарий в базе данных.
            new_comment.save()
    else:
        comment_form = CommentForm()


    return render(
        request, 'blog/post/detail.html', 
        {'post': post,
        'comments': comments,
        'new_comment': new_comment, 
        'comment_form': comment_form}
        )


# класс-обработчик для отображения списка статей
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


# обработчик для получения данных формы и отправки их на почту, если они 
# корректны.
def post_share(request, post_id):
    # Получение статьи с указанным идентификатором и убеждаемся, что статья 
    # опубликована;
    post = get_object_or_404(Post, id=post_id, status='published')
    # переменная sent будет установлена в True после отправки сообщения
    sent = False
    if request.method == 'POST':
        # Форма была отправлена на сохранение.
        # Используем один и тот же обработчик для отображения пустой формы и  
        # обработки  введенных  данных.  Для  разделения  логики  отображения 
        # формы или ее обработки используется запрос request. Заполненная форма 
        # отправляется методом POST. Если метод запроса – GET, необходимо 
        # отобразить пустую форму; если приходит запрос POST, обрабатываем 
        # данные формы и отправляем их на почту.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Все поля формы прошли валидацию.
            cd = form.cleaned_data  #  Если форма валидна, мы получаем 
            # введенные данные с помощью form.cleaned_data. Этот атрибут 
            # является словарем с полями формы и их значениями.

            # ... Отправка электронной почты.
            # добавляем  в  сообщение  абсолютную  ссылку  на  статью.  
            # Полученная абсолютная ссылка будет содержать  HTTP-схему  и  имя 
            # хоста.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            #  сформировали текст  сообщения,  используя данные формы
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            # и, наконец, отправили e-mail по адресам, указанным в поле to формы.
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})