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
    print('Day Chart\t       Night Chart')
    
    for dc, nc in zip(day.day_chart, day.night_chart):
        dayrow = dc[0][1] + '    ' + dc[1].strftime('%H:%M') + '    ' + dc[2].strftime('%H:%M')
        nightrow = '    ' + nc[0][1] + '    ' + nc[1].strftime('%H:%M') + '    ' + nc[2].strftime('%H:%M')
        print(dayrow + nightrow)
    print('')

    print('Sun Markers')
    for marker in day.sun_markers:
        print(marker)

    print('Day Ruler')
    print(day.day_ruler)
    print()
    print('Moon Phase')
    print(day.moon_phase)

day = astrolabe.Day()
report(day)
