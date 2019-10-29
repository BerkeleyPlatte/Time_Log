import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from timelog4app.models import model_factory
from timelog4app.models import Activity
from ..connection import Connection


def get_activity(activity_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Activity)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
                a.name,
                a.active,
                a.app_user_id
        FROM timelog4app_activity a
        WHERE a.id = ?
        """, (activity_id,))

        return db_cursor.fetchone()


@login_required
def activity_details(request, activity_id):
    if request.method == 'GET':
        activity = get_activity(activity_id)

        template = 'activities/detail.html'
        context = {
            'activity': activity
        }

        return render(request, template, context)
    
    if request.method == 'POST':
        form_data = request.POST

   
    if (
        "actual_method" in form_data
        and form_data["actual_method"] == "DELETE"
    ):
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            DELETE FROM timelog4app_activity
            WHERE id = ?
            """, (activity_id,))

        return redirect(reverse('timelog4app:activities'))
