from django.urls import path
from .views import create_assignment

urlpatterns = [
    path('create/', create_assignment, name='create-assignment'),
]