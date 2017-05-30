from datetime import date, datetime, timedelta
import astrolabe
import journalpage

month = 6
datetime_obj = datetime(datetime.now().year, month, 1, 12)
DAY = astrolabe.Day(datetime_object=datetime_obj)
journal = ''
while datetime_obj.month == month:
    journal += journalpage.JournalPage(astroday=DAY).page
    datetime_obj += timedelta(1)
    DAY.set_date(datetime_object=datetime_obj)


journalpage.write_journal(journal, output_file='june.tex')
