from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from cloudinary.uploader import upload
from .models import UserFollow
from .serializers import UserSerializer, UserFollowSerializer, RegisterSerializer, LoginSerializer
from core.views import BaseListCreateView, BaseRetrieveUpdateDestroyView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
User = get_user_model()

# Đăng ký người dùng mới
@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    "EC": 0,
                    "EM": "User created successfully",
                    "DT": {
                        "token": token.key,
                        "user_id": user.id,
                        "username": user.username
                    }
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "EC": 2,
                    "EM": "Database error",
                    "DT": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            "EC": 1,
            "EM": "Validation error",
            "DT": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "EC": 0,
                "EM": "Login successful",
                "DT": {
                    "token": token.key,
                    "user_id": user.id,
                    "username": user.username
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "EC": 1,
            "EM": "Validation error",
            "DT": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# Lấy danh sách người dùng / Thêm người dùng
class UserListCreateView(BaseListCreateView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        password = serializer.validated_data.pop('password', None)
        profile_picture = self.request.FILES.get('profile_picture')

        user = serializer.save(password=make_password(password) if password else None)
        if profile_picture:
            upload_result = upload(profile_picture)
            user.profile_picture = upload_result['secure_url']
            user.save()

# Chi tiết người dùng / Cập nhật / Xóa
class UserDetailUpdateDeleteView(BaseRetrieveUpdateDestroyView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_update(self, serializer):
        password = serializer.validated_data.pop('password', None)
        profile_picture = self.request.FILES.get('profile_picture')

        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()
        if profile_picture:
            upload_result = upload(profile_picture)
            user.profile_picture = upload_result['secure_url']
            user.save()


class UserDetailByIDView(APIView):
    permission_classes = [permissions.AllowAny]  # Bạn có thể thay đổi quyền truy cập nếu cần

    def get(self, request, user_id):
        try:
            # Tìm kiếm người dùng theo ID
            user = User.objects.get(id=user_id)
            # Serialize dữ liệu người dùng
            serializer = UserSerializer(user)
            return Response({
                "EC": 0,
                "EM": "User found",
                "DT": serializer.data
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                "EC": 1,
                "EM": "User not found",
                "DT": None
            }, status=status.HTTP_404_NOT_FOUND)











#-----------------------------------------------------------------------------------------------------------------------
# Follow / Unfollow người dùng
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
            if UserFollow.objects.filter(follower=request.user, followed=user_to_follow).exists():
                return Response({"EC": 1, "EM": "Already following this user", "DT": None}, status=status.HTTP_400_BAD_REQUEST)
            UserFollow.objects.create(follower=request.user, followed=user_to_follow)
            return Response({"EC": 0, "EM": "Follow successful", "DT": None}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"EC": 2, "EM": "User does not exist", "DT": None}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
            follow = UserFollow.objects.filter(follower=request.user, followed=user_to_unfollow)
            if follow.exists():
                follow.delete()
                return Response({"EC": 0, "EM": "Unfollow successful", "DT": None}, status=status.HTTP_200_OK)
            return Response({"EC": 1, "EM": "Not following this user", "DT": None}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"EC": 2, "EM": "User does not exist", "DT": None}, status=status.HTTP_404_NOT_FOUND)

# Danh sách người theo dõi
class UserFollowersListView(BaseListCreateView):
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return UserFollow.objects.filter(followed_id=user_id)

# Danh sách người đang theo dõi
class UserFollowingListView(BaseListCreateView):
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return UserFollow.objects.filter(follower_id=user_id)
