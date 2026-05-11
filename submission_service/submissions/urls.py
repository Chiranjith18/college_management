from django.urls import path
from .views import (
    submit_assignment, edit_submission, my_submissions,
    SubmissionListAPI, SubmissionDetailAPI
)

urlpatterns = [
    path('my/', my_submissions, name='my-submissions'),
    path('submit/<int:assignment_id>/', submit_assignment, name='submit-assignment'),
    path('edit/<int:submission_id>/', edit_submission, name='edit-submission'),
    path('api/', SubmissionListAPI.as_view(), name='submission-list-api'),
    path('api/<int:pk>/', SubmissionDetailAPI.as_view(), name='submission-detail-api'),
]
