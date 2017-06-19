#!/usr/bin/env python3

__author__  = "Aric Maddux"
__version__ = "0.0.1"
__license__ = "MIT"

from datetime import date, datetime
import argparse

UNICODE = 1

def valid_date(string):
    try:
        return datetime.strptime(string, "%m-%d-%Y")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(string)
        raise argparse.ArgumentTypeError(msg)


def print_header(astro_obj):
    print('Report for:')
    print(astro_obj.time.strftime("%m-%d-%Y"))
    print(astro_obj.city)
    print(astro_obj.location.latitude, astro_obj.location.longitude)
    print()

def print_wide_chart(astro_obj):
    print('Day Chart\t       Night Chart')
    spc = '\t'
    for dc, nc in zip(astro_obj.day_chart, astro_obj.night_chart):
        dayrow = dc[0][UNICODE] + spc + dc[1].strftime('%H:%M') + spc + dc[2].strftime('%H:%M')
        nightrow = spc + nc[0][UNICODE] + spc + nc[1].strftime('%H:%M') + spc + nc[2].strftime('%H:%M')
        print(dayrow + nightrow)
    print('')


def print_skinny(astro_obj, night):
    spc = '\t'
    if night:
        print('Night Chart')
        attr = 'night_chart'
    else:
        print('Day Chart')
        attr = 'day_chart'
    for row in getattr(astro_obj, attr):
        print(row[0][UNICODE] + spc + row[1].strftime('%H:%M') + spc + row[2].strftime('%H:%M'))
    print('')


def print_sun_markers(astro_obj):
    print('Sunrise: {}'.format(astro_obj.sun_markers[0].strftime('%H:%M')))
    print('Solar Noon: {}'.format(astro_obj.sun_markers[1].strftime('%H:%M')))
    print('Sunset: {}'.format(astro_obj.sun_markers[2].strftime('%H:%M')))
    print('Next Sunrise: {}'.format(astro_obj.sun_markers[3].strftime('%H:%M')))
    print()


def print_ruler(astro_obj):
    print('Ruler: {}'.format(astro_obj.day_ruler[0]))
    print()


def report(args, astro_obj):    
    if not args.noheader:
        print_header(astro_obj)    
    
    if args.skinny:
        print_skinny(astro_obj, night=False)
        print_skinny(astro_obj, night=True)
    else:
        print_wide_chart(astro_obj)

    if not args.nosun:
        print_sun_markers(astro_obj)
    
    if not args.noruler:
        print_ruler(astro_obj)
    
    print('Moon Phase')
    print(astro_obj.moon_phase)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-nu", "--nounicode",
                        help="Disable unicode",
                        action="store_true",
                        default=False)
    parser.add_argument("-nm", "--nomoon",
                        help="Disable moon phase",
                        action="store_true",
                        default=False)
    parser.add_argument("-nh", "--noheader",
                        help="Disable report header",
                        action="store_true",
                        default=False)
    parser.add_argument("-ns", "--nosun",
                        help="Disable sun markers",
                        action="store_true",
                        default=False)
    parser.add_argument("-nr", "--noruler",
                        help="Disable display of day's ruler",
                        action="store_true",
                        default=False)
    parser.add_argument("-s", "--skinny",
                        help="Display day and night charts separately",
                        action="store_true",
                        default=False)
    parser.add_argument("-d", "--date",
                        help="The date you wish to report on - format MM-DD-YYY",
                        type=valid_date,
                        action="store", 
                        dest="date")
    args = parser.parse_args()
    
    import astrolabe
    if args.date:
        args.date = datetime.replace(args.date, hour=9)
        day = astrolabe.Day(args.date)
    else:
        day = astrolabe.Day()

    if args.nounicode:
        UNICODE = 0
    
    report(args, day)
