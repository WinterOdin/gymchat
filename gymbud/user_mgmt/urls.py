from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CustomUserCreate, BlacklistTokenView

urlpatterns = [
    
    path('/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CustomUserCreate.as_view(), name='create_user'),
    path('logout/blacklist/', BlacklistTokenView.as_view(), name='blacklist'),
    path('users/', UsersListView.as_view(), name='users_list'),
    
]