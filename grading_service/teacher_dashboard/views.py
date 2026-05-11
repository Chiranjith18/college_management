from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.dateparse import parse_datetime
from grading.models import Grade
from grading.forms import GradeForm
from service_clients import get_all_submissions, get_submission, get_all_assignments, get_user

SUBMISSION_SERVICE_BASE_URL = "http://localhost:8003"

def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'role') and request.user.role == 'teacher':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view

@login_required
@teacher_required
def submission_list(request):
    assignments = get_all_assignments()
    teacher_assignment_ids = set()
    assignments_by_id = {}
    for assignment in assignments:
        try:
            assignment_id = int(assignment.get('id'))
            created_by_id = int(assignment.get('created_by_id'))
        except (TypeError, ValueError):
            continue

        assignments_by_id[assignment_id] = assignment
        if created_by_id == request.user.id:
            teacher_assignment_ids.add(assignment_id)
    
    all_submissions = get_all_submissions()
    grades_by_submission_id = {
        grade.submission_id: grade
        for grade in Grade.objects.filter(
            submission_id__in=[s.get('id') for s in all_submissions if s.get('id') is not None]
        )
    }
    user_cache = {}

    submissions = []
    for s in all_submissions:
        try:
            assignment_id = int(s.get('assignment_id'))
        except (TypeError, ValueError):
            continue

        if assignment_id in teacher_assignment_ids:
            assignment = assignments_by_id.get(assignment_id)
            s['assignment'] = assignment

            submitted_at = parse_datetime(s.get('submitted_at', ''))
            s['submitted_at'] = submitted_at

            file_path = s.get('file', '')
            s['file_url'] = f"{SUBMISSION_SERVICE_BASE_URL}{file_path}" if file_path.startswith('/') else file_path
            
            # Fetch student info once per unique student ID.
            student_id = s.get('student_id')
            if student_id not in user_cache:
                user_cache[student_id] = get_user(student_id)
            student = user_cache.get(student_id)
            s['student'] = student
            
            # Use bulk-fetched grades map instead of per-row DB query.
            s['grade'] = grades_by_submission_id.get(s.get('id'))
            
            submissions.append(s)
            
    return render(request, 'teacher_dashboard/submission_list.html', {'submissions': submissions})

@login_required
@teacher_required
def grade_submission(request, submission_id):
    submission_data = get_submission(submission_id)
    if not submission_data:
        raise PermissionDenied
        
    assignments = get_all_assignments()
    assignments_by_id = {}
    for assignment in assignments:
        try:
            assignments_by_id[int(assignment.get('id'))] = assignment
        except (TypeError, ValueError):
            continue

    try:
        submission_assignment_id = int(submission_data.get('assignment_id'))
    except (TypeError, ValueError):
        raise PermissionDenied

    target_assignment = assignments_by_id.get(submission_assignment_id)
    
    try:
        assignment_creator_id = int(target_assignment.get('created_by_id')) if target_assignment else None
    except (TypeError, ValueError):
        assignment_creator_id = None

    if not target_assignment or assignment_creator_id != request.user.id:
        raise PermissionDenied
    
    student = get_user(submission_data['student_id'])
    submission_data['student'] = student
    submission_data['assignment'] = target_assignment
    submission_data['submitted_at'] = parse_datetime(submission_data.get('submitted_at', ''))
    file_path = submission_data.get('file', '')
    submission_data['file_url'] = f"{SUBMISSION_SERVICE_BASE_URL}{file_path}" if file_path.startswith('/') else file_path
    
    grade, created = Grade.objects.get_or_create(submission_id=submission_id, defaults={'marks': 0, 'feedback': ''})
    
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('teacher-dashboard')
    else:
        form = GradeForm(instance=grade)
        
    return render(request, 'teacher_dashboard/grade_submission.html', {
        'submission': submission_data,
        'form': form,
        'created': created
    })
