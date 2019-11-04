# def mil_to_stand(mil):
#     if mil is not None:
#         sliced = mil[:2]
#         if mil[6:] is "AM" or mil[6:] is "PM" or mil[:2] is "AM" or mil[:2] is 'PM':
#             stand = mil
#         elif mil is "00:00:00" or mil is "24:00:00":
#             stand = "12:00 am"
#         elif sliced == 'PM':
#             stand = mil
#         elif mil[:2] is "00":
#             stand = "12" + ":" + mil[3:5] + " " + "am"
#         elif int(mil[:2]) < 12:
#             stand = mil[:5] + " " + "am"
#         elif int(mil[:2]) is 12:
#             stand = "12" + ":" + mil[3:5] + " " + "pm"
#         elif int(mil[:2]) > 12:
#             stand = str(int(mil[:2]) - 12) + ":" + mil[3:5] + " " + "pm"
#         else:
#             stand = "oops, something went wrong!"
#         return stand
#     else:
#         return mil

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

