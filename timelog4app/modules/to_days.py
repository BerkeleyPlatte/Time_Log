def to_days(diffs):
    days_hours_mins = dict()
    total_mins = sum(diffs)
    minutes = int(total_mins % 60)
    divisible_mins = total_mins - minutes
    hours = int(divisible_mins / 60)
    non_divisible_hours = hours % 24
    divisible_hours = hours - non_divisible_hours
    days = int(divisible_hours / 24)
    days_hours_mins['days'] = days
    days_hours_mins['hours'] = non_divisible_hours
    days_hours_mins['minutes'] = minutes
    return days_hours_mins
