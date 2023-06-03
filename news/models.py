from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.contrib.auth import get_user_model
from .managers import UserManager
from django.shortcuts import render, get_object_or_404, redirect

User = get_user_model()


class User(AbstractBaseUser, PermissionsMixin):
    SUPERADMIN = 1
    NEWS_EDITOR = 2
    READER = 3

    ROLE_TYPES = (
        (SUPERADMIN, 'Супер-администратор'),
        (NEWS_EDITOR, 'Новостной редактор'),
        (READER, 'Читатель'),
    )

    role = models.IntegerField('Выберите роль', choices=ROLE_TYPES)
    username = models.CharField('Логин', max_length=50, unique=True)
    first_name = models.CharField("ФИО", max_length=100, blank=True, null=True)
    email = models.EmailField("Почта", default="email@mail.com", blank=True, null=True)
    date_joined = models.DateTimeField("Дата присоединения", default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, verbose_name='Статус доступа')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    groups = models.ManyToManyField(
        Group,
        verbose_name='Группы',
        blank=True,
        help_text='Группы, к которым принадлежит этот пользователь. '
                  'Пользователь получает все разрешения, предоставленные каждой из его групп.',
        related_name='news_user_set',
        related_query_name='news_user'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='Разрешения пользователя',
        blank=True,
        help_text='Конкретные разрешения для этого пользователя.',
        related_name='news_user_set',
        related_query_name='news_user'
    )


class News(models.Model):
    URGENT_NEWS = 1
    NEWS_OF_THE_DAY = 2

    NEWS_TYPES = (
        (URGENT_NEWS, 'СРОЧНЫЕ НОВОСТИ'),
        (NEWS_OF_THE_DAY, 'НОВОСТЬ ДНЯ'),
    )

    title = models.CharField('Заголовок', max_length=255, default='')
    text = models.TextField('Описание', default='')
    date_post = models.DateTimeField('Дата создания поста', default=timezone.now)
    news_type = models.IntegerField('Тип новости', choices=NEWS_TYPES)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title
    
    def news_detail(request, news_id):
        news = get_object_or_404(News, id=news_id)
        return render(request, 'news_detail.html', {'news': news})


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField('Комментарий')
    created_at = models.DateTimeField('Дата создания', default=timezone.now)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий к новости "{self.news.title}"'
    
# def news_detail(request, news_id):
#     news = get_object_or_404(News, id=news_id)
#     return render(request, 'news_detail.html', {'news': news})

def add_comment(request):
    if request.method == 'POST':
        news_id = request.POST.get('news_id')
        content = request.POST.get('content')

        news = get_object_or_404(News, id=news_id)

        # Создание нового комментария
        comment = Comment.objects.create(news=news, content=content, created_at=timezone.now())
        comment.save()
        # Дополнительная логика, если необходимо

        return redirect('news_detail', news_id=news_id)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь создавший пост', null=True, blank=True, related_name='posts')
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='Новость', null=True, blank=True, related_name='posts')
    date_post = models.DateTimeField(default=timezone.now, verbose_name='Дата создания поста')
    title = models.CharField(max_length=200, default='', verbose_name='Заголовок')
    content = models.TextField(default='', verbose_name='Содержание')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='authored_posts')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])
