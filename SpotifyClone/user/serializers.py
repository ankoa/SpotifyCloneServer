from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserFollow
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )
    is_staff = serializers.BooleanField(default=False)  # Truy cập Admin
    is_superuser = serializers.BooleanField(default=False)  # Toàn quyền Admin
    user_permissions = serializers.PrimaryKeyRelatedField(
        queryset=User.user_permissions.rel.related_model.objects.all(),
        many=True,
        required=False
    )
    groups = serializers.PrimaryKeyRelatedField(
        queryset=User.groups.rel.related_model.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "profile_picture", "bio", "date_of_birth", "country",
            "password", "is_staff", "is_superuser", "user_permissions", "groups"
        ]

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url  
        return None

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "profile_picture", "bio", "date_of_birth", "country"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])  # Hash mật khẩu
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        return {"user": user}
class UserFollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    followed = UserSerializer(read_only=True)

    class Meta:
        model = UserFollow
        fields = ['id', 'follower', 'followed', 'followed_at']
