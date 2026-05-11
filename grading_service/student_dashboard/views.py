from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from service_clients import get_all_assignments, get_all_submissions
from grading.models import Grade

def student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'role') and request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view

@login_required
@student_required
def student_dashboard_view(request):
    all_assignments = get_all_assignments()
    now = timezone.now()
    
    # Fetch all submissions by this student via API
    all_submissions = get_all_submissions()
    student_submissions = {
        s['assignment_id']: s 
        for s in all_submissions if s['student_id'] == request.user.id
    }
    
    # Process assignments
    processed_assignments = []
    submitted_count = 0
    
    for a in all_assignments:
        submission = student_submissions.get(a['id'])
        a['is_submitted'] = submission is not None
        
        # Check for grade in local DB
        if submission:
            grade = Grade.objects.filter(submission_id=submission['id']).first()
            a['grade'] = grade
            
        deadline = timezone.datetime.fromisoformat(a['deadline'].replace('Z', '+00:00'))
        a['is_overdue'] = deadline < now
        
        if a['is_submitted']:
            submitted_count += 1
        processed_assignments.append(a)
    
    return render(request, 'student_dashboard/dashboard.html', {
        'assignments': processed_assignments,
        'total_count': len(processed_assignments),
        'submitted_count': submitted_count
    })
