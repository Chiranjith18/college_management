from django.shortcuts import render, redirect
from .forms import AssignmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics
from .models import Assignment
from .serializers import AssignmentSerializer

# Dummy decorator since accounts app is gone
def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'role') and request.user.role == 'teacher':
            return view_func(request, *args, **kwargs)
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    return _wrapped_view

@login_required
@teacher_required
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.created_by_id = request.user.id
            assignment.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('http://localhost:8004/dashboard/teacher/')
    else:
        form = AssignmentForm()

    return render(request, 'assignments/create_assignment.html', {'form': form})

class AssignmentListAPI(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class AssignmentDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer