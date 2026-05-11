from django.urls import path
from .views import create_assignment, AssignmentListAPI, AssignmentDetailAPI

urlpatterns = [
    path('create/', create_assignment, name='create-assignment'),
    path('api/', AssignmentListAPI.as_view(), name='assignment-list-api'),
    path('api/<int:pk>/', AssignmentDetailAPI.as_view(), name='assignment-detail-api'),
]