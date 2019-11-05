import datetime

def mil_to_stand(mil):
    stand = datetime.datetime.strptime(mil[:5], '%H:%M').strftime('%I:%M %p')
    return stand
