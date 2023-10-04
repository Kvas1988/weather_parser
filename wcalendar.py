import json
import calendar
from datetime import datetime, timedelta
from dateutil import relativedelta

class CalendarRange():
    start_date: datetime
    end_date: datetime

    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"

class Calendar():
    backlog_max: datetime
    last_date: datetime
    backlog: bool

    def __init__(self, backlog=False):
        self.backlog = backlog

        with open("calendar.json", "r") as f:
            data = json.load(f)
            self.backlog_max = datetime.strptime(data['backlog_max'], "%d.%m.%Y")
            self.last_date = datetime.strptime(data['last_date'], "%d.%m.%Y")
            self.start_date = self.set_start_date()

    def __iter__(self):
        return self

    def __next__(self):
        if self.backlog:
            if self.start_date < self.last_date:
                next = self.start_date
                end = self.get_last_date()
                self.start_date += relativedelta.relativedelta(months=1, day=1)
                return CalendarRange(next, end)
        raise StopIteration

    def set_start_date(self) -> datetime:
        if self.backlog:
            return self.backlog_max + timedelta(days=1)

        return self.last_date + timedelta(days=1)

    def get_start_date(self) -> datetime:
        return self.start_date

    def get_last_date(self) -> datetime:
        dt = self.get_start_date()
        if self.backlog:
            last_day_of_month = calendar.monthrange(dt.year, dt.month)[1]
            dt = datetime(dt.year, dt.month, last_day_of_month)

        return dt
