from datetime import datetime, timedelta,date
import astrolabe

the_date = datetime(date.today().year, date.today().month, date.today().day, 12)
calendar = astrolabe.Day()
calendar = astrolabe.Day(the_date)

print('Phase Calendar')
for day in range(365):    
    if calendar.moon_phase != None:
        print(calendar.moon_phase, calendar.time, calendar.day_ruler[0])
    the_date += timedelta(1)
    calendar.set_date(the_date)
