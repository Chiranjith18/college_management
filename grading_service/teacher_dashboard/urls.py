from django.urls import path
from . import views

urlpatterns = [
    path('', views.submission_list, name='teacher-dashboard'),
    path('<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
]
