from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Создание своего менеджера модели, вместо Objects который по-умолчанию
class PublishedManager(models.Manager):
    # Метод  менеджера  get_queryset()  возвращает  QuerySet,  который  будет 
    # выполняться.
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


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

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

