from django.urls import path, include

from .views import (
    UserListCreateView, UserDetailUpdateDeleteView,
    FollowUserView, UserFollowersListView, UserFollowingListView,RegisterView,LoginView,UserDetailByIDView
)

urlpatterns = [
    #  API lấy danh sách tất cả người dùng và thêm mới
    path('users/', UserListCreateView.as_view(), name='user-list-create'),

    #  API lấy thông tin chi tiết user theo ID, cập nhật, xóa
    path('users/<int:pk>/', UserDetailUpdateDeleteView.as_view(), name='user-detail-update-delete'),

    #  API Follow / Unfollow user theo ID
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),

    #  API lấy danh sách những người follow một user
    path('users/<int:user_id>/followers/', UserFollowersListView.as_view(), name='user-followers-list'),

    #  API lấy danh sách những người mà user đang follow
    path('users/<int:user_id>/following/', UserFollowingListView.as_view(), name='user-following-list'),

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path('api/users/<int:user_id>/', UserDetailByIDView.as_view(), name='user-detail-by-id'),

]
