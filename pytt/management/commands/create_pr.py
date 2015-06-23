from pytt.models import ParityReference
from django.core.management.base import NoArgsCommand
from django.db import connection, transaction

import calendar
import datetime
import copy

class Command(NoArgsCommand):
    """This command calculates parity for each week of the studying year,
    starting on 1st Septmber. Rules are:
    From first September to the first Sunday including, the week is dubbed as
    even one. Then all the weeks are being alternated till the next 1st Sept.
    The command  writes to the DB corresponding model.

    Command should be executed once a year. Crontab:
    0 0 1 9 * python /pytt/manage.py create_pr
    """
    @transaction.atomic
    def handle_noargs(self, **options):
        def get_week_days(year, week):
            """Get date period depending on the year and week number.
            Params:
                year (int): year
                week (int): week to calculate from
            Returns:
                (datetime.date): week Monday date
                (datetime.date): week Sunday date
            """
            begin = datetime.date(year, 1, 1)
            if begin.weekday() > 3:
                begin = begin + datetime.timedelta(7 - begin.weekday())
            else:
                begin = begin - datetime.timedelta(begin.weekday())
            dlt = datetime.timedelta(days=(week - 1) * 7)
            return begin + dlt, begin + dlt + datetime.timedelta(days=6)

        cursor = connection.cursor()
        # Drop previous stuff in DB
        ParityReference.objects.all().delete()
        cursor.execute('ALTER TABLE pytt_parityreference AUTO_INCREMENT 1;')
        # Getting current month, to calulcate the September
        current_time = datetime.datetime.now()
        begin_year = current_time.year
        # Year starts in SEPTEMBER
        # If update is being called in the second part of the year
        # we should decrease year by one
        if 1 <= current_time.month <= 8:
            begin_year -= 1
        begin_date = datetime.date(begin_year, 9, 1)
        end_date = copy.deepcopy(begin_date)
        # Calulating the week from 1.09 to first Sunday
        while not end_date.weekday() == 6:
            end_date = end_date.replace(day=end_date.day + 1)
        weekno = begin_date.isocalendar()[1]
        is_even = True

        # Leap year check. If year is leap, ACADEMIC year is 90 weeks, else 89
        all_weeks = 89 if not calendar.isleap(begin_year) else 90

        # Some magic, but somehow Python jumps over 52nd week to 1st week
        # of the next year
        # Write the models
        for week in xrange(weekno, all_weeks):
            start, end = get_week_days(begin_year, week)
            ParityReference(**dict(zip(['begin_day', 'end_day', 'is_even'],
                                       [start, end, is_even]))).save()
            is_even = not is_even



