from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User, auth

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request=request, user=user)
            return redirect('/activities')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'registration/login.html')
    