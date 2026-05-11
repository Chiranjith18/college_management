from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from grading.models import Grade
from grading.forms import GradeForm
from service_clients import get_all_submissions, get_submission, get_all_assignments, get_user

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
    teacher_assignment_ids = [a['id'] for a in assignments if a['created_by_id'] == request.user.id]
    
    all_submissions = get_all_submissions()
    
    submissions = []
    for s in all_submissions:
        if s['assignment_id'] in teacher_assignment_ids:
            assignment = next((a for a in assignments if a['id'] == s['assignment_id']), None)
            s['assignment'] = assignment
            
            # Fetch student info via API
            student = get_user(s['student_id'])
            s['student'] = student
            
            # Check for grade in local DB
            grade = Grade.objects.filter(submission_id=s['id']).first()
            s['grade'] = grade
            
            submissions.append(s)
            
    return render(request, 'teacher_dashboard/submission_list.html', {'submissions': submissions})

@login_required
@teacher_required
def grade_submission(request, submission_id):
    submission_data = get_submission(submission_id)
    if not submission_data:
        raise PermissionDenied
        
    assignments = get_all_assignments()
    target_assignment = next((a for a in assignments if a['id'] == submission_data['assignment_id']), None)
    
    if not target_assignment or target_assignment['created_by_id'] != request.user.id:
        raise PermissionDenied
    
    student = get_user(submission_data['student_id'])
    submission_data['student'] = student
    submission_data['assignment'] = target_assignment
    
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
