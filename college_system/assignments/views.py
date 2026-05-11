from django.shortcuts import render, redirect
from .forms import AssignmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from accounts.decorators import teacher_required

@login_required
@teacher_required
def create_assignment(request):

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.created_by = request.user
            assignment.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('create-assignment')
    else:
        form = AssignmentForm()

    return render(request, 'assignments/create_assignment.html', {'form': form})