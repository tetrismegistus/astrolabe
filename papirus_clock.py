import sys
import time
from datetime import datetime, date, timedelta

import astrolabe
from papirus import PapirusTextPos


class Clock:
    def __init__(self):
        self.calendar = astrolabe.Day()
        self.text = PapirusTextPos(False, rotation=0)
        self.text.partialUpdates = True
        self.Time()

    def current_ruler(self):
        current_time = self.calendar.convert_zone(datetime.now(), self.calendar.time_zone, self.calendar.time_zone)
        day = int(date.today().day)
        if current_time <= self.calendar.day_chart[0][1]:
            day -= 1
            self.calendar.set_date(datetime_object=datetime(date.today().year, date.today().month, day, 12))
        elif current_time >= self.calendar.night_chart[11][2]:
            self.calendar.set_date(datetime_object=datetime(date.today().year, date.today().month, day, 12))

        merged_chart = self.calendar.day_chart + self.calendar.night_chart
        for row in merged_chart:
            if row[1] <= current_time <= row[2]:
                next_index = (self.calendar.find_hour_index(row[0]) + 1) % 7
                return [row[0], row[2], self.calendar.HOUR_RULERS[next_index]]

        print(current_time)
        for x in merged_chart:
            print(str(x[1]), str(x[2]))

    def Time(self):
        current_ruler = self.current_ruler()

        date_string = '{} {}'.format(self.calendar.day_ruler.unicode, time.strftime('%m/%d'))
        self.text.AddText(date_string, 10, 10, size=50, Id="date")
        hour_time = datetime.now().strftime('%H:%M')
        time_string = '{} {}'.format(current_ruler[0].unicode, hour_time)
        self.text.AddText(time_string, 10, 100, size=50, Id="time")
        self.text.UpdateText("date", date_string)
        self.text.UpdateText("time", time_string)
        self.text.WriteAll()

def main():
    clock = Clock()
    while True:
        time.sleep(30)
        clock.Time()

if __name__ == '__main__':
    main()
