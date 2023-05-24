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

from .models import Post
from .serializers import PostSerializer
from .forms import PostForms
from .permissions import SuperAdmin
from rest_framework import viewsets
from .models import User, News
from .serializers import UserSerializer, NewsSerializer
from django.shortcuts import render
from django.http import HttpResponse

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

def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

def post_single(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_single.html', {'post': post})

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

class NEWS_EDITORView(ListAPIView):
    permission_classes = [SuperAdmin]

    def get(self, request, *args, **kwargs):
        return Response(data={'success': 'Поздравляю, вы действительно суперадмин'}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

def news_list(request):
    # Your code to fetch and display a list of news
    return HttpResponse("News list")

def news_detail(request, news_id):
    # Your code to fetch and display a specific news item
    return HttpResponse(f"News detail for id: {news_id}")    