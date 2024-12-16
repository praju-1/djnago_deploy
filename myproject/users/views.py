from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Registration
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {'error': 'Username already exists'})
        elif len(password) < 6:
            return render(request, 'users/register.html', {'error': 'Password must be at least 6 characters'})
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('feed')
    return render(request, 'users/register.html')

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/feed/')
        else:
            # messages.error(request, "Invalid credentials")
            return render(request, 'users/login.html', {'error': 'Invalid username or password'})
    return render(request, 'users/login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('/users/login/')
