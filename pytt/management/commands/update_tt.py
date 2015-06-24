""" Universal command to update timetables
"""

import logging

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.management import call_command
from django.db import transaction

from pytt.models import *
from pytt.parse import TTXMLParser
from pytt.fetch import SSUFetcher


class Command(NoArgsCommand):
    """This command runs full TT database update each update interval, basing
    on cron file. It drops all the data, downloads it,
    parses and stores. Transactions are atomic, so all the DB update is going
    to executed in one step, so users can access the service even during update
    times
    """
    _logger = logging.getLogger()
    _parser = TTXMLParser()
    _fetcher = SSUFetcher(propfile=settings.PROP_FILE)

    @transaction.atomic
    def handle_noargs(self, **options):
        def check_teacher(teacher):
            """Check if the teacher is already in the DB. If their
            name is shorter, then update to newer one, if the newer is longer
            Params:
                teacher (int): ssu_id of the teacher
            Returns:
                (int): exit code, status
                (obj or None): updated teacher or None if the teacher to be
            added.
            """
            try:
                _teacher = Teacher.objects.get(ssu_id=teacher.ssu_id)
                if len(teacher.name) > len(_teacher.name):
                    return -1, _teacher
            except Teacher.DoesNotExist:
                return 0, None
            return 1, _teacher
        response = self._fetcher.fetch_general()
        if not response['success']:
            self._logger.critical('Fetching department list failed. Something '
                                  'wrong with SSU endpoint, aborting update: '
                                  '%s', response)
            return

        Teacher.objects.all().delete()
        Subgroup.objects.all().delete()
        Subject.objects.all().delete()
        Cell.objects.all().delete()
        Group.objects.all().delete()
        Department.objects.all().delete()
        self._logger.info('Database drop completed')
        call_command('reset_index')
        self._logger.info('Update interval set to %d hours',
                          settings.CURRENT_UPDATE_INTERVAL)
        for pddata in self._parser.parse_department_data(response['text']):
            department = Department(**pddata)
            department.save()
            self._logger.info('Added department: %s ', department)
            # RawGroupData
            rgdata = self._fetcher.fetch_department(department.tag)
            if rgdata['success']:
                # ParsedGroupData
                for pgdata in self._parser.parse_group_data(rgdata['text']):
                    group = Group(**pgdata)
                    group.department = department
                    self._logger.info('Added group: %s', group)
                    group.save()
                    for entry in self._parser.parse_lesson_data(rgdata['text'],
                                                                group):
                        cell = Cell()
                        cell.group = group

                        dtp, _ = DayTimeParity.objects.get_or_create(
                            **{x: entry[x]
                               for x in ['day', 'time', 'parity']})

                        cell.dtp = dtp

                        subj, _ = Subject.objects.get_or_create(
                            **{x: entry[x]
                               for x in ['name', 'begin_date', 'end_date']})
                        cell.subject = subj

                        new_teacher = Teacher(
                            **{'ssu_id': entry['teacher_id'],
                               'name': entry['teacher_name']})
                        # add teacher
                        # if -1 then name is better, update it
                        # if 0 then teacher does not exist, create it
                        # if 1 then teacher exists, can use _teacher
                        status, teacher = check_teacher(new_teacher)
                        if status == -1:
                            teacher.name = new_teacher.name
                            teacher.save()
                        elif not status:
                            new_teacher.save()
                            teacher = new_teacher

                        subgr, _  = Subgroup.objects.get_or_create(
                            **{'name': entry['subgroup'],
                               'location': entry['location'],
                               'teacher': teacher,
                               'activity': entry['activity']})

                        cell.subgroup = subgr
                        cell.save()
            else:
                self._logger.critical('Fetching groups for %s (%s) failed',
                                      department.tag,
                                      rgdata)

