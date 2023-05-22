from django.shortcuts import render
from .models import News

def news_list(request):
    news = News.objects.all()
    return render(request, 'news_list.html', {'news': news})

def news_detail(request, pk):
    news = News.objects.get(pk=pk)
    return render(request, 'news_detail.html', {'news': news})
