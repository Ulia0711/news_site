from django.urls import path
from rest_framework import routers
from .views import (
    news_list, news_detail,add_comment,
    UserView, NewsViewSet, PostView,
    create_news,
)

router = routers.DefaultRouter()
router.register(r'users', UserView)
router.register(r'news', NewsViewSet)

urlpatterns = [
    path('posts/', PostView.as_view({'get': 'list', 'post': 'create'}), name='post_list'),
    path('news/', news_list, name='news_list'),
    path('', news_list, name='index'),
    path('news/<int:news_id>/', news_detail, name='news_detail'),
    path('add_comment/', add_comment, name='add_comment'),
]

# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('api/posts/', PostView.as_view({'get': 'list', 'post': 'create'}), name='post-list'),
#     path('api/posts/<int:pk>/', PostView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='post-detail'),
#     path('', views.news_list, name='news_list'),
#     path('news/<int:news_id>/', news_detail, name='news_detail'),
#     path('post/<int:post_id>/', views.post_detail, name='post_detail'),
#     path('news/add_comment/', add_comment, name='add_comment'),
#     path('app/', include('news_site.urls')),
#     path('create_news/', create_news, name='create_news'),
# ]
