from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from assignments.models import Assignment
from .models import Submission
from .forms import SubmissionForm

from django.utils import timezone
from accounts.decorators import student_required

@login_required
@student_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Check if a submission already exists
    existing_submission = Submission.objects.filter(student=request.user, assignment=assignment).first()
    if existing_submission:
        return redirect('edit-submission', submission_id=existing_submission.id)

    # Check if deadline has passed
    if assignment.deadline < timezone.now():
        messages.error(request, f'Submission for "{assignment.title}" is closed. Deadline has passed.')
        return redirect('student-dashboard')
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.save()
            messages.success(request, f'Assignment "{assignment.title}" submitted successfully!')
            return redirect('student-dashboard')
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
    submission = get_object_or_404(Submission, id=submission_id, student=request.user)
    assignment = submission.assignment
    
    # Check if deadline has passed
    if assignment.deadline < timezone.now():
        messages.error(request, f'Editing for "{assignment.title}" is closed. Deadline has passed.')
        return redirect('student-dashboard')
    
    # Check if already graded
    if hasattr(submission, 'grade'):
        messages.error(request, f'Cannot edit submission for "{assignment.title}" as it has already been graded.')
        return redirect('student-dashboard')

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, f'Submission for "{assignment.title}" updated successfully!')
            return redirect('student-dashboard')
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
    submissions = Submission.objects.filter(student=request.user).select_related('assignment', 'grade').order_by('-submitted_at')
    return render(request, 'submissions/my_submissions.html', {
        'submissions': submissions,
        'now': timezone.now()
    })


