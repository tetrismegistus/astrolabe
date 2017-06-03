# !/usr/bin/env python3

from collections import namedtuple
from datetime import datetime, timedelta, date
from dateutil import tz
import ephem
from geopy.geocoders import GoogleV3 


def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


class Day(object):

    Planet = namedtuple('Planet', ['name', 'unicode', 'bg_color', 'fg_color'])
    LUNAR = Planet('Moon', u'\u263D', 'violet', 'white')
    MARS = Planet('Mars', u'\u2642', 'red', 'white')
    MERCURY = Planet('Mercury', u'\u263F', 'orange', 'white')
    JUPITER = Planet('Jupiter', u'\u2643', 'blue', 'white')
    VENUS = Planet('Venus', u'\u2640', 'green', 'white')
    SATURN = Planet('Saturn', u'\u2644', 'black', 'white')
    SOLAR = Planet('Sun', u'\u2609', 'yellow', 'white')
    DAY_RULERS = [LUNAR, MARS, MERCURY, JUPITER, VENUS, SATURN, SOLAR]
    HOUR_RULERS = [SATURN, JUPITER, MARS, SOLAR, VENUS, MERCURY, LUNAR]

    def __init__(self,
                 datetime_object=datetime(date.today().year, date.today().month, date.today().day, 12),
                 location_string='Indianapolis, IN',
                 zone_string='America/Indianapolis'):
        geo_locator = GoogleV3()
        self.city = location_string
        self.location = geo_locator.geocode(self.city)
        self.time_zone = tz.gettz(zone_string)
        self.utc_zone = tz.gettz('UTC')
        self.set_date(datetime_object)

    def set_date(self, datetime_object):
        self.time = datetime_object
        self.observer = ephem.Observer()
        self.setup_observer()
        self.sun_markers = self.set_sun_markers()
        self.day_ruler = self.DAY_RULERS[self.time.weekday()]
        self.day_chart = self.build_chart(night=0)
        self.night_chart = self.build_chart(night=1)
        self.moon_phase = self.set_moon_phase()

    # noinspection PyMethodMayBeStatic
    def convert_zone(self, time_object, from_zone, to_zone):
        time = time_object.replace(tzinfo=from_zone)
        return time.astimezone(to_zone)

    # noinspection PyDunderSlots
    def setup_observer(self):
        self.observer.pressure = 0
        self.observer.horizon = '-0:34'
        self.observer.name = self.location
        self.observer.date = self.convert_zone(self.time, self.time_zone, self.utc_zone)
        self.observer.lat, self.observer.lon = str(self.location.latitude), str(self.location.longitude)

    def set_sun_markers(self):
        sun = ephem.Sun()
        transit = self.observer.next_transit(sun)
        if transit.datetime().day > self.observer.datetime().day:
            transit = self.observer.previous_transit(sun)
        markers = [str(self.observer.previous_rising(sun)),
                   str(self.observer.next_transit(sun)),
                   str(self.observer.next_setting(sun)),
                   str(self.observer.next_rising(sun))]
        for i in range(len(markers)):
            utc = datetime.strptime(markers[i], '%Y/%m/%d %H:%M:%S')
            markers[i] = self.convert_zone(utc, self.utc_zone, self.time_zone)
            markers[i] = markers[i].replace(second=0, microsecond=0)
        if markers[1].day > self.observer.datetime().date().day:

        return markers

    def find_hour_length(self, end, start):
        # this will return interval of planetary hours
        elapsed_time = end - start
        seconds = elapsed_time.total_seconds()
        length = int(seconds / 12)
        return timedelta(seconds=length)

    def find_hour_index(self, ruler):
        for hour in range(7):
            if self.HOUR_RULERS[hour] == ruler:
                return hour

    def build_chart(self, night=0):
        ruler_int = self.time.weekday()  # will be used to find first hour ruler and subsequent
        if night == 0:
            # building day table
            hour_length = self.find_hour_length(self.sun_markers[2], self.sun_markers[0])
            hour_ruler = self.DAY_RULERS[ruler_int]
            hour_index = self.find_hour_index(ruler=hour_ruler)
            start = self.sun_markers[0]
        else:
            # building night table
            # DAY CHART MUST BE CALLED FIRST OR CTHULHU WILL EAT YOUR COMPUTER
            hour_length = self.find_hour_length(self.sun_markers[3], self.sun_markers[2])
            # this trick is obscure
            hour_index = (self.find_hour_index(self.day_chart[11][0]) + 1) % 7
            start = self.sun_markers[2]
        planet_table = []
        for hour in range(12):
            # each entry in the table will be a list that contains
            # [0] hour_ruler tuple
            # [1] start_time of hour
            # [2] end_time of hour
            row = [self.HOUR_RULERS[hour_index], start]
            end = start + hour_length
            row.append(end)
            planet_table.append(row)
            start = end 
            hour_index = (hour_index + 1) % 7
        return planet_table

    def set_moon_phase(self):
        moon = ephem.Moon()
        moon.compute(self.observer)
        current_date = self.observer.date
        ref_date = current_date.datetime().date()
        # I know this is ugly, but this is the most accurate way I could get a moon phase using 
        # pyephem's moon phase lookup. other solutions involved estimating based on last new moon
        # which kinda loses the accuracy of pyephem, which is why I chose the library in the first place.
        # I am SURE there is more elegant way, and am totally open to suggestions
        moon_cal = {ephem.next_new_moon(current_date).datetime().date()              : 'New',
                    ephem.previous_new_moon(current_date).datetime().date()          : 'New',
                    ephem.next_first_quarter_moon(current_date).datetime().date()    : 'First Quarter',
                    ephem.previous_first_quarter_moon(current_date).datetime().date(): 'First Quarter',
                    ephem.next_full_moon(current_date).datetime().date()             : 'Full',
                    ephem.previous_full_moon(current_date).datetime().date()         : 'Full',
                    ephem.next_last_quarter_moon(current_date).datetime().date()     : 'Last Quarter',
                    ephem.previous_last_quarter_moon(current_date).datetime().date() : 'Last Quarter'}
        if ref_date in moon_cal.keys():
            return moon_cal[ref_date]
        nearest_date = nearest(list(moon_cal.keys()), ref_date)
        ref_phase = moon_cal[nearest_date]
        cycle = ['New', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous', 'Full', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent']
        index = cycle.index(ref_phase)
        if ref_date > nearest_date:
            return cycle[(index + 1) % len(cycle)]
        elif ref_date < nearest_date:
            return cycle[(index - 1) % len(cycle)]
