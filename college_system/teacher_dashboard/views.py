from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from assignments.models import Assignment
from submissions.models import Submission
from grading.models import Grade
from grading.forms import GradeForm
from accounts.decorators import teacher_required

@login_required
@teacher_required
def submission_list(request):
    # Get all submissions for assignments created by this teacher
    submissions = Submission.objects.filter(assignment__created_by=request.user).order_by('-submitted_at')
    return render(request, 'teacher_dashboard/submission_list.html', {'submissions': submissions})

@login_required
@teacher_required
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, assignment__created_by=request.user)
    
    # Try to get existing grade or create a new one
    grade, created = Grade.objects.get_or_create(submission=submission, defaults={'marks': 0, 'feedback': ''})
    
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('teacher-dashboard')
    else:
        form = GradeForm(instance=grade)
        
    return render(request, 'teacher_dashboard/grade_submission.html', {
        'submission': submission,
        'form': form,
        'created': created
    })
