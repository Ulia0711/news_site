from django.contrib import admin
from .models import News, Comment, Post, User
from .forms import CustomUserChangeForm

class PostAdmin(admin.ModelAdmin):
    list_display=('user','title','text','date_post')
    list_filter=('user','date_post')
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(User, UserAdmin)
