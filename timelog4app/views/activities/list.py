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
            where a.active = false
            and a.app_user_id = ?
            order by a.name asc
            """, (request.user.id,))

            all_activities = db_cursor.fetchall()

        template_name = 'activities/list.html'

        return render(request, template_name, {'all_activities': all_activities}, {'time_allocation_list': time_allocation_list})

    elif request.method == 'POST':
        form_data = request.POST
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
            select name, id
            from timelog4app_activity 
            where app_user_id = ?
            """, (request.user.id,))

            dataset = db_cursor.fetchall()
            activities = set()

            for row in dataset:
                activity = Activity()
                activity.id = row['id']
                activity.name = row['name']

                activities.add(activity.name)

            if form_data['title'] not in activities:

                with sqlite3.connect(Connection.db_path) as conn:
                    db_cursor = conn.cursor()

                    db_cursor.execute("""
                    INSERT INTO timelog4app_activity
                    (name, active, app_user_id)
                    values (?, ?, ?)
                    """,
                                      (form_data['title'], False, request.user.id))

            else:
                with sqlite3.connect(Connection.db_path) as conn:
                    db_cursor = conn.cursor()
                    db_cursor.execute("""
                    update timelog4app_activity
                    set active = false
                    where name = ?
                    """, (form_data['title'],))

        return redirect(reverse('timelog4app:activities'))
