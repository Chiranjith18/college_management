from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from rest_framework import generics
from .models import Submission
from .forms import SubmissionForm
from .serializers import SubmissionSerializer
from .service_clients import get_assignment
from datetime import datetime

# Dummy decorator since accounts app is gone
def student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'role') and request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view

@login_required
@student_required
def submit_assignment(request, assignment_id):
    assignment = get_assignment(assignment_id)
    if not assignment:
        messages.error(request, 'Assignment not found.')
        return redirect('http://localhost:8004/dashboard/student/') # Redirect to grading service dashboard

    # Check if a submission already exists
    existing_submission = Submission.objects.filter(student_id=request.user.id, assignment_id=assignment_id).first()
    if existing_submission:
        return redirect('edit-submission', submission_id=existing_submission.id)

    # Check if deadline has passed
    deadline = datetime.fromisoformat(assignment['deadline'].replace('Z', '+00:00'))
    if deadline < timezone.now():
        messages.error(request, f'Submission for "{assignment["title"]}" is closed. Deadline has passed.')
        return redirect('http://localhost:8004/dashboard/student/')
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student_id = request.user.id
            submission.assignment_id = assignment_id
            submission.save()
            messages.success(request, f'Assignment "{assignment["title"]}" submitted successfully!')
            return redirect('http://localhost:8004/dashboard/student/')
    else:
        form = SubmissionForm()
    
    return render(request, 'submissions/submit_assignment.html', {
        'form': form,
        'assignment': assignment,
        'is_edit': False
    })

@login_required
@student_required
def edit_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, student_id=request.user.id)
    assignment = get_assignment(submission.assignment_id)
    
    if not assignment:
        messages.error(request, 'Assignment not found.')
        return redirect('http://localhost:8004/dashboard/student/')

    # Check if deadline has passed
    deadline = datetime.fromisoformat(assignment['deadline'].replace('Z', '+00:00'))
    if deadline < timezone.now():
        messages.error(request, f'Editing for "{assignment["title"]}" is closed. Deadline has passed.')
        return redirect('http://localhost:8004/dashboard/student/')
    
    # Check if already graded (this will eventually need an API call to Grading Service)
    # For now we'll check if a grade exists in our shared DB if we want, but let's stick to APIs later.

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, f'Submission for "{assignment["title"]}" updated successfully!')
            return redirect('http://localhost:8004/dashboard/student/')
    else:
        form = SubmissionForm(instance=submission)
    
    return render(request, 'submissions/submit_assignment.html', {
        'form': form,
        'assignment': assignment,
        'submission': submission,
        'is_edit': True
    })

@login_required
@student_required
def my_submissions(request):
    submissions = Submission.objects.filter(student_id=request.user.id).order_by('-submitted_at')
    # Enhancing submissions with assignment info via API
    enriched_submissions = []
    for s in submissions:
        assignment = get_assignment(s.assignment_id)
        enriched_submissions.append({
            'id': s.id,
            'assignment': assignment,
            'submitted_at': s.submitted_at,
            'file': s.file
        })

    return render(request, 'submissions/my_submissions.html', {
        'submissions': enriched_submissions,
        'now': timezone.now()
    })

class SubmissionListAPI(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class SubmissionDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
