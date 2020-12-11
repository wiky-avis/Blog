from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# сторонее приложение
from taggit.managers import TaggableManager

# Создание своего менеджера модели, вместо Objects который по-умолчанию
class PublishedManager(models.Manager):
    # Метод  менеджера  get_queryset()  возвращает  QuerySet,  который  будет 
    # выполняться.
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

# модель для сохранения статей
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts'
        )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft'
        )
    
    objects = models.Manager() # Менеджер по умолчанию.
    published = PublishedManager() # Наш новый менеджер.
    
    # Менеджер tags позволит нам добавлять, получать список и удалять теги для 
    # объектов статей.
    tags = TaggableManager()

    # В Django есть соглашение о том, что метод модели get_absolute_url() 
    # должен возвращать канонический URL объекта
    def get_absolute_url(self):
        return reverse(
            'blog:post_detail', args=[self.publish.year, 
            self.publish.month, self.publish.day, self.slug]
            )
        # Мы будем использовать метод get_absolute_url() в HTML-шаблонах, 
        # чтобы получать ссылку на статью.


    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'
        ordering = ('-publish',)

    def __str__(self):
        return self.title


# модель для сохранения комментариев
class Comment(models.Model):
    # Модель  Comment  содержит  ForeignKey  для  привязки  к  определенной  
    # статье.Это отношение определено как «один ко многим», т.к. одна статья 
    # может иметь множество комментариев, но каждый комментарий может быть 
    # оставлен только для одной статьи. Атрибут related_name позволяет получить 
    # доступ к комментариям конкретной статьи. Теперь мы сможем обращаться к 
    # статье из комментария, используя запись comment.post, и к комментариям 
    # статьи при помощи post.comments.all().
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    # поле created для сортировки комментариев в хронологическом порядке
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # булевое поле active, для того чтобы была возможность скрыть некоторые 
    # комментарии (например, содержащие оскорбления)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)