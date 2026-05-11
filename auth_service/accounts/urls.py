from django.urls import path
from .views import signup_view, CustomLoginView, UserDetailAPI, logout_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/users/<int:pk>/', UserDetailAPI.as_view(), name='user-detail-api'),
]