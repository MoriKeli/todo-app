from datetime import datetime, timedelta
from calendar import HTMLCalendar
from todo_app.models import Tasks

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        # self.tasks = events
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        tasks_per_day = events.filter(date_due__day=day)
        d = ''
        for task in tasks_per_day:
            d += f'<li>{task.task}</li>'

        if day != 0:
            return f'<td><span class="date">{day}</span><ul>{d}</ul></td>'
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr>{week}</tr>'
    
    def formatmonth(self, withyear=True):
        tasks = Tasks.objects.filter(date_due__year=self.year, date_due__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar"\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, tasks)}\n'
        return cal
