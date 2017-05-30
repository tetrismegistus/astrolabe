#!/usr/bin/env python3

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
        print(row[0][1], '    ', row[1].strftime('%H:%M'), '    ', row[2].strftime('%H:%M'))
    print('')

    print('Night Chart')
    for row in day.night_chart:
        print(row[0][1], '    ', row[1].strftime('%H:%M'), '    ', row[2].strftime('%H:%M'))
    print('')

    print('Sun Markers')
    for marker in day.sun_markers:
        print(marker)

    print('Day Ruler')
    print(day.day_ruler)
    print()
    print('Moon Phase')
    print(day.moon_phase)

day = astrolabe.Day(datetime.now())
report(day)
