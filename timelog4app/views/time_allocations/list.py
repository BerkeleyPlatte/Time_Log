import sqlite3
from django.shortcuts import render
from timelog4app.models import Time_Allocation
from timelog4app.models import model_factory
from ..connection import Connection
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
import datetime


@login_required
def time_allocation_list(request):
    todays_date = str(datetime.datetime.now().strftime("%x"))
    current_time = str(datetime.datetime.now().strftime("%X"))

    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Time_Allocation)
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select DISTINCT
                a.name,
                ta.start_time,
                ta.stop_time
            from
                timelog4app_activity a,
                timelog4app_time_allocation ta,
                auth_user au
            where
                ta.date = ?
                and ta.activity_id = a.id
                and a.app_user_id = ?
            order by
                ta.start_time ASC;
            """, (todays_date, request.user.id,))

            all_time_allocations = db_cursor.fetchall()

        template_name = 'time_allocations/list.html'

        return render(request, template_name, {'all_time_allocations': all_time_allocations})

    elif request.method == 'POST':
        if ("actual_method" in request.POST and request.POST["actual_method"] == "PUT"):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                destination = 'timelog4app:activities'

                db_cursor.execute(""" 
                UPDATE timelog4app_time_allocation
                set stop_time = ?
                where id = ?
                and date = ?
                """, (current_time, request.POST['activity_id_edited'], todays_date))

        else:
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                destination = 'timelog4app:time_allocations'

                db_cursor.execute("""
                INSERT INTO timelog4app_time_allocation
                (start_time, stop_time, date, activity_id)
                values (?, null, ?, ?)
                """, (current_time, todays_date, request.POST['activity_id']))

        return redirect(reverse(destination))
