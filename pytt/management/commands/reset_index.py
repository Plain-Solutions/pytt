""" Reset incdices of main tables"""

from django.core.management.base import NoArgsCommand
from django.db import connection


class Command(NoArgsCommand):
    """ This command restarts all the indices of the following
    tables. The command is executed automatically on each update
    """
    def handle_noargs(self, **options):
        cursor = connection.cursor()
        seqs = ['pytt_cell',
                'pytt_department',
                'pytt_group',
                'pytt_subgroup',
                'pytt_subject',
                'pytt_teacher',
                ]
        for seq in seqs:
            cursor.execute('ALTER TABLE %s AUTO_INCREMENT 1;' % seq)
