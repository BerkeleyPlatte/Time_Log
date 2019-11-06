def times_diff(start, stop):
    if stop is None:
        start_mins = 0
        stop_mins = 0
    else:
        start_mins = (int(start[:2]) * 60) + int(start[3:5])
        stop_mins = (int(stop[:2]) * 60) + int(stop[3:5])
    diff_in_mins = stop_mins - start_mins
    return diff_in_mins