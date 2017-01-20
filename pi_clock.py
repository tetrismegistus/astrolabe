import sys
import time
import astrolabe
from datetime import datetime, date, timedelta
from PyQt5.QtWidgets import QMainWindow, QLCDNumber, QApplication, QWidget, QLabel, QGridLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont


class ClockPanel(QLCDNumber):
    def __init__(self):
        super(ClockPanel, self).__init__()

    def update_display(self, background, foreground, display_string):
        self.display(time.strftime(display_string))
        style_string = 'QLCDNumber { background-color : ' + background + '; color : ' + foreground + '; }'
        self.setStyleSheet(style_string)
        self.setSegmentStyle(QLCDNumber.Flat)


class ClockLabel(QLabel):
    def __init__(self):
        super(ClockLabel, self).__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont('Arial', 50, QFont.Bold))

    def update_label(self, background, foreground, label_string):
        style_string = 'QLabel { background-color : ' + background + '; color : ' + foreground + '; }'
        self.setStyleSheet(style_string)
        self.setText(label_string)


class Clock(QWidget):
    def __init__(self):
        super(Clock, self).__init__()
        self.calendar = astrolabe.Day()
        self.date_lcd = ClockPanel()
        self.date_label = ClockLabel()
        self.hour_lcd = ClockPanel()
        self.hour_label = ClockLabel()
        self.next_lcd = ClockPanel()
        self.next_label = ClockLabel()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)
        layout = QGridLayout()
        layout.addWidget(self.date_label, 0, 0)
        layout.addWidget(self.date_lcd, 0, 1)
        layout.addWidget(self.hour_label, 1, 0)
        layout.addWidget(self.hour_lcd, 1, 1)
        layout.addWidget(self.next_label, 2, 0)
        layout.addWidget(self.next_lcd, 2, 1)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        self.setLayout(layout)
        self.Time()

    def Time(self):
        now = self.calendar.convert_zone(datetime.now(), self.calendar.time_zone, self.calendar.time_zone)
        if now <= self.calendar.day_chart[0][1]:
            day = date.today() - timedelta(hours=24)
            day = day.day
            self.calendar.set_date(datetime_object=datetime(date.today().year, date.today().month, day, 12))

        current_ruler = self.calendar.current_ruler()
        background_color = current_ruler[0].bg_color
        foreground_color = current_ruler[0].fg_color
        self.hour_lcd.update_display(background_color, foreground_color, time.strftime('%H:%M'))
        self.hour_label.update_label(background_color, foreground_color, current_ruler[0].unicode)

        background_color = self.calendar.day_ruler.bg_color
        foreground_color = self.calendar.day_ruler.fg_color
        self.date_lcd.update_display(background_color, foreground_color, time.strftime('%m/%d'))
        self.date_label.update_label(background_color, foreground_color, self.calendar.day_ruler.unicode)

        background_color = current_ruler[2].bg_color
        foreground_color = current_ruler[2].fg_color
        hour_time = current_ruler[1].strftime('%H:%M')
        self.next_label.update_label(background_color, foreground_color, current_ruler[2].unicode)
        self.next_lcd.update_display(background_color, foreground_color, hour_time)


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent, Qt.FramelessWindowHint)
        self.clock = Clock()
        self.setCentralWidget(self.clock)
        self.showMaximized()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()



def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
