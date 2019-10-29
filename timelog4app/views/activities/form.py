import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection


@login_required
def activity_form(request):
    if request.method == 'GET':
        template = 'activities/form.html'

        return render(request, template)
