from django.urls import path
from .views import student_dashboard_view

urlpatterns = [
    path('', student_dashboard_view, name='student-dashboard'),
]
