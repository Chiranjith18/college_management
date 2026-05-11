from django.urls import path
from . import views

urlpatterns = [
    path('submissions/', views.submission_list, name='teacher-dashboard'),
    path('submissions/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
]
