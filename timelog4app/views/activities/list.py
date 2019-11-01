import sqlite3
from django.shortcuts import render
from timelog4app.models import Activity
from timelog4app.models import model_factory
from ..connection import Connection
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from timelog4app.views.time_allocations.list import time_allocation_list

@login_required
def activity_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Activity)
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                a.id,
                a.name,
                a.active,
                a.app_user_id
            from timelog4app_activity a
            where a.app_user_id = ?
            """, (request.user.id,))

            all_activities = db_cursor.fetchall()

        template_name = 'activities/list.html'

        return render(request, template_name, {'all_activities': all_activities}, {'time_allocation_list': time_allocation_list})

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO timelog4app_activity
            (name, active, app_user_id)
            values (?, ?, ?)
            """,
                              (form_data['title'], False, request.user.id))

        return redirect(reverse('timelog4app:activities'))
