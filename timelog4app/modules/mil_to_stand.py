import datetime


def mil_to_stand(mil):

    if mil is not None:
        sliced = mil[:2]
        if mil[6:] is "AM" or mil[6:] is "PM" or mil[:2] is "AM" or mil[:2] is 'PM':
            stand = mil
        else:

            stand = datetime.datetime.strptime(mil[:5], '%H:%M').strftime('%I:%M %p')

        return stand
    else:
        return mil
