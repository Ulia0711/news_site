from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password
from .managers import UserManager

class Role(models.Model):
    SUPERADMIN = 1
    NEWS_EDITOR = 2
    READER = 3

    ROLE_TYPES = (
        (SUPERADMIN, 'Супер-администратор'),
        (NEWS_EDITOR, 'Новостной редактор'),
        (READER, 'Читатель'),
    )

    name = models.CharField('Название', max_length=50, choices=ROLE_TYPES)

    def __str__(self):
        return self.name
    
class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    id = models.AutoField(primary_key=True)
    username = models.CharField('Логин', max_length=50, unique=True)
    first_name = models.CharField("ФИО", max_length=100, blank=True, null=True)
    email = models.EmailField("Почта", default="email@mail.com", blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='Роль')
    date_joined = models.DateTimeField("Дата присоединения", default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, verbose_name='Статус доступа')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []


    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. '
                  'A user will get all permissions granted to each of their groups.',
        related_name='news_users'  # Add a unique related_name
    )

    # Specify a unique related_name for user_permissions
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='news_users'  # Add a unique related_name
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
    
class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь создавший пост', null=True, blank=True, related_name='posts')
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='Новость', null=True, blank=True, related_name='posts')
    date_post = models.DateTimeField(default=timezone.now, verbose_name='Дата создания поста')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return str(self.news)
