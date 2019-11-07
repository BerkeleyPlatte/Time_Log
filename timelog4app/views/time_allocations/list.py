import datetime
import sqlite3
from django.shortcuts import render
from timelog4app.models import Time_Allocation
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from ..connection import Connection
from timelog4app.models import model_factory
from timelog4app.modules.mil_to_stand import mil_to_stand


@login_required
def time_allocation_list(request):
    todays_date = datetime.datetime.now().strftime("%x")
    current_time = datetime.datetime.now().strftime('%X')

    if request.method == 'GET':
        if request.GET.get("desired_date") is None:
            with sqlite3.connect(Connection.db_path) as conn:
                conn.row_factory = sqlite3.Row
                db_cursor = conn.cursor()

                db_cursor.execute("""
                select DISTINCT
                    ta.id,
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

                all_time_allocations = []
                dataset = db_cursor.fetchall()

                for row in dataset:
                    time_allocation = Time_Allocation()
                    time_allocation.id = row['id']
                    time_allocation.name = row['name']
                    time_allocation.start_time = mil_to_stand(row['start_time'])
                    time_allocation.stop_time = mil_to_stand(row['stop_time'])

                    all_time_allocations.append(time_allocation)
        else:

            with sqlite3.connect(Connection.db_path) as conn:
                form_data = request.GET.get("desired_date")

                conn.row_factory = sqlite3.Row
                db_cursor = conn.cursor()
                db_cursor.execute("""
                select DISTINCT
                    ta.id,
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
                """, (form_data, request.user.id,))

                all_time_allocations = []
                dataset = db_cursor.fetchall()

                for row in dataset:
                    time_allocation = Time_Allocation()
                    time_allocation.id = row['id']
                    time_allocation.name = row['name']
                    time_allocation.start_time = mil_to_stand(
                        row['start_time'])
                    time_allocation.stop_time = mil_to_stand(row['stop_time'])

                    all_time_allocations.append(time_allocation)

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
                """, (current_time, request.POST['activity_id_edited'],))

        elif ("actual_method" in request.POST and request.POST["actual_method"] == "DELETE"):

            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                destination = 'timelog4app:time_allocations'

                db_cursor.execute("""
                    DELETE FROM timelog4app_time_allocation
                    WHERE id = ?
                """, (request.POST['id_to_delete'],))

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
