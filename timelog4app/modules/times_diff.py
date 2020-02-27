def times_diff(start, stop):
    start_hours = int(start[:2])
    start_mins = int(start[3:5])
    stop_hours = int(stop[:2])
    stop_mins = int(stop[3:5])
    if stop_hours < start_hours:
        mins_before_midnight = (1440 - (start_hours * 60)) + start_mins
        mins_after_midnight = (stop_hours * 60) + stop_mins
        diff_in_mins = mins_before_midnight + mins_after_midnight
    else:
        total_start_mins = (start_hours * 60) + start_mins
        total_stop_mins = (stop_hours * 60) + stop_mins
        diff_in_mins = total_stop_mins - total_start_mins
    return diff_in_mins