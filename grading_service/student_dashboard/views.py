from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.dateparse import parse_datetime
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
    student_submissions = {}
    for submission in all_submissions:
        try:
            if int(submission.get('student_id')) == request.user.id:
                student_submissions[int(submission.get('assignment_id'))] = submission
        except (TypeError, ValueError):
            continue
    
    # Process assignments
    processed_assignments = []
    submitted_count = 0
    
    for a in all_assignments:
        try:
            assignment_id = int(a.get('id'))
        except (TypeError, ValueError):
            continue

        submission = student_submissions.get(assignment_id)
        a['is_submitted'] = submission is not None
        
        # Check for grade in local DB
        if submission:
            grade = Grade.objects.filter(submission_id=submission['id']).first()
            a['grade'] = grade
            
        deadline_raw = a.get('deadline')
        deadline = parse_datetime(deadline_raw) if deadline_raw else None
        if deadline and timezone.is_naive(deadline):
            deadline = timezone.make_aware(deadline, timezone.get_current_timezone())
        a['deadline'] = deadline
        a['is_overdue'] = bool(deadline and deadline < now)
        
        if a['is_submitted']:
            submitted_count += 1
        processed_assignments.append(a)
    
    return render(request, 'student_dashboard/dashboard.html', {
        'assignments': processed_assignments,
        'total_count': len(processed_assignments),
        'submitted_count': submitted_count
    })
