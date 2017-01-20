from datetime import date, datetime
import astrolabe

def report(day):
    print()
    print('Report for:')
    print(str(day.time))
    print(day.city)
    print(day.location.latitude, day.location.longitude)
    print()
    print('Day Chart')
    for row in day.day_chart:
        print(row[0][1], '    ', row[1], '    ', row[2])
    print('')

    print('Night Chart')
    for row in day.night_chart:
        print(row[0][1], '    ', row[1], '    ', row[2])
    print('')

    print('Sun Markers')
    for marker in day.sun_markers:
        print(marker)

    print()
    print('Current Ruler and end time')
    ruler = day.current_ruler()
    print(ruler[0][0], ruler[1], ruler[2])
    print()
    print('Day Ruler')
    print(day.day_ruler)
    print()
    print('Moon Phase')
    print(day.moon_phase)


day = astrolabe.Day(datetime_object=datetime(date.today().year, date.today().month, date.today().day, 12))
report(day)

'''
print()
print('Phase Calendar')
for mydate in range(2, 32):
    print(day.moon_phase, day.time, day.day_ruler[0])
    day.set_date(datetime_object=datetime(date.today().year, date.today().month, mydate, 12))
'''

print(day.night_chart)
import pdb; pdb.set_trace()