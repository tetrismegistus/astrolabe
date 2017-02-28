from datetime import date, datetime
import astrolabe
import journalpage

MONTH = 2
DATE = 1
DAY = astrolabe.Day(datetime_object=datetime(date.today().year, MONTH, DATE, 12))
journal = ''
for loopday in range(1, 29):
    DAY.set_date(datetime_object=datetime(date.today().year, MONTH, loopday, 12))
    journal += journalpage.JournalPage(astroday=DAY).page


journalpage.write_journal(journal, output_file='february.tex')
