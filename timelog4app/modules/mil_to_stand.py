import datetime

def mil_to_stand(mil):
    if mil is not None:
        return datetime.datetime.strptime(mil[:5], '%H:%M').strftime('%I:%M %p')
    else:
        return mil