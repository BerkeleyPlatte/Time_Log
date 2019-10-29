import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register_user(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    '''
    if request.method == "GET":
        template_name = 'registration/register.html'
        return render(request, template_name, {})

    elif request.method == "POST":
        form_data = request.POST

        new_user = User.objects.create_user(
            username=form_data['username'],
            email=form_data['email'],
            password=form_data['password'],
            first_name=form_data['first_name'],
            last_name=form_data['last_name']
        )

        authenticated_user = authenticate(
            username=form_data['username'], password=form_data['password'])

        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            return redirect(reverse('timelog4app:activities'))

        else:
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
