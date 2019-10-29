import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from .details import get_activity


@login_required
def activity_form(request):
    if request.method == 'GET':
        template = 'activities/form.html'

        return render(request, template)


@login_required
def activity_edit_form(request, activity_id):

    if request.method == 'GET':
        activity = get_activity(activity_id)

        template = 'activities/form.html'
        context = {
            'activity': activity,
        }

        return render(request, template, context)
