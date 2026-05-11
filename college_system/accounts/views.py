from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib import messages


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now login.')
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


from assignments.models import Assignment

def home_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('student-dashboard')
        elif request.user.role == 'teacher':
            return redirect('teacher-dashboard')
        
    assignments = Assignment.objects.all()
    return render(request, 'home.html', {'assignments': assignments})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'