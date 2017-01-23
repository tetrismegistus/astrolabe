from datetime import date, datetime
import astrolabe

day = astrolabe.Day()
day = astrolabe.Day(datetime_object=datetime(date.today().year, date.today().month, 1, 12))

print('Phase Calendar')
for my_date in range(2, 32):
    print(day.moon_phase, day.time, day.day_ruler[0])
    day.set_date(datetime_object=datetime(date.today().year, date.today().month, my_date, 12))