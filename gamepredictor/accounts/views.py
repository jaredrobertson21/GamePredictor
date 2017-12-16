from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def user_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('home')
        else:
            return render(request, 'account/login.html',
                          {'error': 'The username and password combination does not exist'})
    else:
        return render(request, 'accounts/login.html')


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def user_signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                print("Inside try")
                return render(request, 'accounts/signup.html', {'error': 'Username has already been taken'})
            except:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                print("Inside except")
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'accounts/signup.html')
