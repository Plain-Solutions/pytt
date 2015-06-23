""" Store time limits centralized
"""

import logging
from pytt.models import TimeReference
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    """ This command creates TimeReference objects for each departments,
    where classes times differ. Now (2014) there are only three differing
    departments. Geologic College, Electronics College (YABLOKO) and SSU itself
    Command creates data for /times request.

    Command should be run on each database drop or on the first deployment
    python /pytt/manage.py create_tr
    """
    _logger = logging.getLogger()

    def handle_noargs(self, **options):
        main_times = [('08:20', '09:50'),
                      ('10:00', '11:35'),
                      ('12:05', '13:40'),
                      ('13:50', '15:25'),
                      ('15:35', '17:10'),
                      ('17:20', '18:40'),
                      ('18:45', '20:05'),
                      ('20:10', '21:30')]

        yabloko_times = [('08:45', '10:15'),
                         ('10:25', '11:55'),
                         ('12:25', '13:55'),
                         ('14:05', '15:35')]

        geo_times = [('09:00', '10:30'),
                     ('10:40', '12:10'),
                     ('12:30', '14:00'),
                     ('14:10', '15:40'),
                     ('15:50', '17:20'),
                     ('17:30', '19:00'),
                     ('19:10', '20:40')]

        all_times = [main_times, yabloko_times, geo_times]

        TimeReference.objects.all().delete()

        for dep_time in range(3):
            i = 0
            for lesson in all_times[dep_time]:
                TimeReference(**{'dtype': dep_time,
                                 'sequence': i,
                                 'begin': lesson[0],
                                 'end': lesson[1]}).save()
                i += 1

        self._logger.info('Added time limits records')
