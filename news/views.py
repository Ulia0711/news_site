from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework import status
from .models import Post, News, Comment, User
from .serializers import PostSerializer, UserSerializer, NewsSerializer
from .forms import PostForms
from .permissions import SuperAdmin
from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from django.http import HttpResponse
from django.views.generic import DetailView
from django.http import HttpResponseNotAllowed

class PostView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title', 'text']
    search_fields = ['title', 'text']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, created_at=timezone.now())

# Функция index отображает шаблон 'index.html'
def index(request):
    return render(request, 'index.html')

# Функция post_single отображает отдельный пост по его идентификатору (pk)
def post_single(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_single.html', {'post': post})

# Функция post_form отображает форму для создания нового поста
def post_form(request):
    if request.method == "POST":
        form = PostForms(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.created_at = timezone.now()
            post.save()
            return redirect('single', pk=post.pk)
    else:
        form = PostForms()
    return render(request, 'post_add.html', {'form': form})

# Класс NewsDetailView отображает детали новости и список всех новостей
class NewsDetailView(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получите все новости и добавьте их в контекст
        context['all_news'] = News.objects.all()
        
        return context
    
# Класс SUPERADMINView возвращает ответ, если пользователь является супер-администратором
class SUPERADMINView(ListAPIView):
    permission_classes = [SuperAdmin]

    def get(self, request, *args, **kwargs):
        return Response(data={'success': 'Поздравляю, вы действительно Супер-администратор'}, status=status.HTTP_200_OK)

# Класс NEWS_EDITORView возвращает ответ, если пользователь является новостным редактором
class NEWS_EDITORView(ListAPIView):
    permission_classes = [SuperAdmin]

    def get(self, request, *args, **kwargs):
        return Response(data={'success': 'Поздравляю, вы действительно Новостной редактор'}, status=status.HTTP_200_OK)

# Класс READERView возвращает ответ, если пользователь является читателем
class READERView(ListAPIView):
    permission_classes = [SuperAdmin]

    def get(self, request, *args, **kwargs):
        return Response(data={'success': 'Поздравляю, вы действительно Читатель'}, status=status.HTTP_200_OK)

# Класс TokenObtainPairView для получения пары токенов доступа и обновления
class TokenObtainPairView(TokenObtainSlidingView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer

# Класс TokenRefreshView для обновления пары токенов доступа и обновления
class TokenRefreshView(TokenRefreshSlidingView):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer

# Класс RegisterView для регистрации нового пользователя
class RegisterView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        role = self.request.data.get('role')
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.role = role
        user.save()

# Функция register для обработки регистрации пользователя
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        role_type = [
            {'value': User.SUPERADMIN, 'label': 'Супер-администратор'},
            {'value': User.NEWS_EDITOR, 'label': 'Новостной редактор'},
            {'value': User.READER, 'label': 'Читатель'},
        ]

        serializer = UserSerializer(data={
            'username': username,
            'email': email,
            'password': password,
            'role': role_type,
        })

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.role = role
            user.save()

            return redirect('success')

# Класс UserView для управления пользователями
class UserView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'get_current_user':
            permission_classes = [AllowAny]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def get_current_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

# Класс NewsViewSet для управления новостями
class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

# Функция news_list отображает список всех новостей

def news_list(request):
    news = News.objects.all()  # Получаем список всех новостей из базы данных
    context = {'news': news}  # Создаем контекст шаблона с данными о новостях
    return render(request, 'news_list.html', context)


# Функция post_list отображает список всех постов
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

# Функция post_detail отображает детали поста по его идентификатору (post_id)
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post': post})

# Функция create_news обрабатывает создание новости
def create_news(request):
    if request.method == 'POST':
        # Получите данные из запроса
        title = request.POST.get('title')
        text = request.POST.get('text')
        news_type = request.POST.get('news_type')

        new_news = News(title=title, text=text, news_type=news_type)
        new_news.save()  # Сохраните новость в базе данных

    return redirect('news_list')  # Перенаправьте пользователя на список новостей

def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'news': news})

def single(request, news_id):
    news = get_object_or_404(News, id=news_id)
    context = {
        'news': news
    }
    return render(request, 'single.html', context)

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
    else:
        return HttpResponse(status=405)
