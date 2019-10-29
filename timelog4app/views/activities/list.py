import sqlite3
from django.shortcuts import render
from timelog4app.models import Activity
from ..connection import Connection
from django.contrib.auth.decorators import login_required

@login_required
def activity_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                a.id,
                a.name,
                a.active,
                a.app_user_id
            from timelog4app_activity a
            """)

            all_activities = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                activity = Activity()
                activity.id = row['id']
                activity.name = row['name']
                activity.active = row['active']
                activity.app_user_id = row['app_user_id']

                all_activities.append(activity)

        template = 'activities/list.html'
        context = {
            'all_activities': all_activities
        }

        return render(request, template, context)
