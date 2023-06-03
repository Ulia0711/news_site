from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer, TokenObtainPairSerializer
)
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import serializers
from .models import User, News, Post

class TokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, *args, **kwargs):
        data = super().validate(*args, **kwargs)

        if not self.user.is_active:
            raise AuthenticationFailed({
                'detail': f"Пользователь {self.user.username} был деактивирован!"
            }, code='user_deleted')

        data['id'] = self.user.id
        data['username'] = self.user.username

        return data

class TokenRefreshSerializer(TokenRefreshSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])

        try:
            user = User.objects.get(
                pk=refresh.payload.get('user_id')
            )
        except ObjectDoesNotExist:
            raise serializers.ValidationError({
                'detail': f"Пользователь был удалён!"
            }, code='user_does_not_exists')

        if user.blocked:
            raise AuthenticationFailed({
                'detail': f"Пользователь {user.username} был заблокирован!"
            }, code='user_deleted')

        data['id'] = user.id
        data['username'] = user.username

        return data

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_TYPES)  # Поле выбора роли

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = '__all__'

    def get_user_info(self, obj):
        serializer = GetUserSerializer(obj.user)
        return serializer.data

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
