from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    NEWS_TYPES = [
        ('URGENT', 'СРОЧНЫЕ НОВОСТИ'),
        ('DAILY', 'НОВОСТЬ ДНЯ'),
        # Добавьте другие типы новостей по вашему усмотрению
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    news_type = models.CharField(max_length=10, choices=NEWS_TYPES)
    # Добавьте другие поля, необходимые для вашей модели новости

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    # Добавьте другие поля, необходимые для вашей модели комментария

# Добавьте модель пользователя, если вам нужно добавить дополнительные поля для пользователей.
