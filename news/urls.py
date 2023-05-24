from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, NewsViewSet, PostView
from news.views import news_list, news_detail

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'news', NewsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/posts/', PostView.as_view({'get': 'list', 'post': 'create'}), name='post-list'),
    path('api/posts/<int:pk>/', PostView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='post-detail'),
]
