import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from timelog4app.models import model_factory
from timelog4app.models import Activity
from timelog4app.models import Time_Allocation
from timelog4app.modules.times_diff import times_diff
from timelog4app.modules.to_days import to_days
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


def get_activity_allocations(activity_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select ta.start_time, ta.stop_time
        from timelog4app_time_allocation ta, timelog4app_activity a
        where ta.activity_id = a.id and ta.stop_time is not null and a.id = ?
        """, (activity_id,))

        activity_specific_allocations = []
        rows = db_cursor.fetchall()
        
        for each in rows:
            time_allocation = Time_Allocation()
            time_allocation.diff_in_mins = times_diff(
                each['start_time'], each['stop_time'])
            activity_specific_allocations.append(time_allocation)
        
        return to_days([each.diff_in_mins for each in activity_specific_allocations])


@login_required
def activity_details(request, activity_id):
    if request.method == 'GET':
        activity = get_activity(activity_id)
        totals = get_activity_allocations(activity_id)

        template = 'activities/detail.html'
        context = {
            'activity': activity,
            'totals': totals
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE timelog4app_activity
                SET name = ?
                WHERE id = ?
                """, (form_data['title'], activity_id,))

            return redirect(reverse('timelog4app:activities'))

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                update timelog4app_activity
                set active = true
                WHERE id = ?
                """, (activity_id,))

            return redirect(reverse('timelog4app:activities'))
