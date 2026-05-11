from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import SignupForm
from django.contrib.auth import login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User


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


class UserDetailAPI(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


def home_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('http://localhost:8004/dashboard/student/')
        elif request.user.role == 'teacher':
            return redirect('http://localhost:8004/dashboard/teacher/')
    return render(request, 'home.html', {'assignments': []})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True   # auto-redirect if already logged in

    def get_redirect_url(self):
        """Allow cross-port redirects for our microservices setup."""
        next_url = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, ''),
        )
        # Trust localhost redirects (our own services)
        if next_url and 'localhost' in next_url:
            return next_url
        return ''

    def get_default_redirect_url(self):
        """After login, send users to the grading service dashboard."""
        user = self.request.user
        if hasattr(user, 'role'):
            if user.role == 'student':
                return 'http://localhost:8004/dashboard/student/'
            elif user.role == 'teacher':
                return 'http://localhost:8004/dashboard/teacher/'
        return '/'


@csrf_exempt
def logout_view(request):
    """Simple logout that works with both GET and POST, no CSRF needed."""
    auth_logout(request)
    return redirect('http://localhost:8001/accounts/login/')