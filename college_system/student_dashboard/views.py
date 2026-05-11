from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from assignments.models import Assignment
from submissions.models import Submission

from django.utils import timezone
from accounts.decorators import student_required

@login_required
@student_required
def student_dashboard_view(request):
    assignments = Assignment.objects.all().order_by('-deadline')
    now = timezone.now()
    
    # Fetch all submissions by this student for these assignments, including grades
    submissions = {
        s.assignment_id: s 
        for s in Submission.objects.filter(student=request.user).select_related('grade')
    }
    
    # Add submission and deadline info to each assignment object
    submitted_count = 0
    for assignment in assignments:
        submission = submissions.get(assignment.id)
        assignment.submission = submission
        assignment.is_submitted = submission is not None
        assignment.is_overdue = assignment.deadline < now
        if assignment.is_submitted:
            submitted_count += 1
    
    return render(request, 'student_dashboard/dashboard.html', {
        'assignments': assignments,
        'total_count': assignments.count(),
        'submitted_count': submitted_count
    })
