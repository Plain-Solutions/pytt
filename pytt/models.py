"""Models describe all the entities in the project"""

from django.db import models


class TimeReference(models.Model):
    """TimeReference is a model for request /times
    Contains information about sequences and times correlation
    Fields:
        dtype (int): type of department (see Department)
        sequence (int): number of class during the day (0-8)
        begin (str): start of the class HH-MM (24hr)
        end (str): finish of the class HH-MM (24hr)
    Ordered by dtype, then sequence, which is enough
    """
    dtype = models.PositiveSmallIntegerField()
    sequence = models.PositiveSmallIntegerField()
    begin = models.CharField(max_length=5)
    end = models.CharField(max_length=5)

    class Meta:
        ordering = ['dtype', 'sequence']


class ParityReference(models.Model):
    """ParityReference is automatically caluclated parity table. It starts on
    the September, 1st, each year and then is being alternated.
    Fields:
        begin_day (datetime.date): date, when the week starts formatted as
    YYYY-MM-DD
        end_day (datetime.date): date, when the week finishes (including the
    day) formatted as YYYY-MM-DD
        is_even (bool): parity of the week, 1 for EVEN and 0 for ODD
    Ordering by dates
    """
    begin_day = models.DateField()
    end_day = models.DateField()
    is_even = models.BooleanField(default=True)
    class Meta:
        ordering = ['begin_day', 'end_day']

class Department(models.Model):
    """Department is a set of groups. They can differ by name and corresponding
    tag, which is used for addressing in SSU TT. Also they can contain some
    infromational text string. Finally, they differ by timetable type, called
    dtype and used in TimeReference
    Fields:
        name (string): official name of the department
        tag (string): internal SSU short string used for navigation, basicly
    some sort of acronym
        dtype (int): type of department according to TimeReference table
        info (string): text with infromation provided by department
    Ordering by type of department, then by it's official name in Russian
    """
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=10)
    dtype = models.PositiveSmallIntegerField()
    info = models.TextField()

    class Meta:
        ordering = ['dtype', 'name']

    def __str__(self):
        return 'Name: %s Tag: %s Type: %d' % (self.name,
                                              self.tag,
                                              self.dtype)


class Group(models.Model):
    """Group is an addressable set of cells. Group contains all the cells
    (hence, all the classes) of the group in department. They differ by
    academic grade (specs, bacheors, masters, pre-docs) and mode of study
    (full-time, evening)
    Fields:
        department (obj, id): ForeignKey to Department object
        name (string): name of the group
        gform (int): mode of study
        gtype (int): academic grade
    gfrom-gtype
    00 - full-time specialist
    01 - full-time bachelor
    02 - full-time masters
    03 - full-time pre-doc
    20 - evening specialist
    21 - evening bachelor
    22 - evening masters (if any, not found yet)
    0-1 - colleges
    PyTT ignores part-timers as there are no timetable for them yet
    Ordering by name
    """
    department = models.ForeignKey('Department')
    name = models.CharField(max_length=60)
    gform = models.SmallIntegerField()
    gtype = models.SmallIntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '(%s)Name: %s Type: %s%s' % (self.department.tag,
                                            self.name,
                                            self.gform,
                                            self.gtype)


class DayTimeParity(models.Model):
    """DayTimeParity represents time coordinates, there are three of them.
    Fields:
        day (int): day of the week (0-5)
        time (int): aka sequence # of class (0-8(5))
        parity (str): parity written description nom, denom or full
    Ordered by day, then by time, and finally by parity
    """
    day = models.PositiveSmallIntegerField()
    time = models.PositiveSmallIntegerField()
    parity = models.CharField(max_length=5)

    class Meta:
        ordering = ['day', 'time', 'parity']


class Teacher(models.Model):
    """Teacher model is quite simple.
    Fields:
        ssu_id (int): internal ID used by SSU
        name (str): full name of the teacher
    Ordered by name, then by id
    """
    ssu_id = models.PositiveIntegerField()
    name = models.CharField(max_length=120)

    class Meta:
        ordering = ['name', 'ssu_id']


class Subgroup(models.Model):
    """ Subgroup is an entity, which connects teacher and location to Cell.
    Fields:
        name (str): name of subgroup, often empty
        location (str): name of the room/building
        teacher (obj, id): foreing key to Teacher instance
        activity (str): type of class: practice, lecture or lab class
    """
    name = models.CharField(max_length=80)
    location = models.CharField(max_length=80)
    teacher = models.ForeignKey('Teacher')
    activity = models.CharField(max_length=10)


class Subject(models.Model):
    """ Subject is an entity which controls global time limits of class
    and connects its name to Cell
    Fields:
        name (str): name of the subject
        begn_date, end_date (int): epoch seconds, when this or that class
    is being held
    """
    name = models.CharField(max_length=200)
    begin_date = models.IntegerField()
    end_date = models.IntegerField()


class Cell(models.Model):
    """Cell is the main unit of v3 API. This is a cell like in timetables, but
        without any merging. Merge is part of the View, which is our
        mobile apps. Cell answers the question, "What is happening
        on such day, at such time in such week (parity)?" and returns
        multiple answers.
        All the fields are connectors to corresponding entities.
    Fields:
        group (obj, id): group, which has this or that subject in that Cell
        dtp (obj, id): date-time-parity object
        subject (obj, id): subject instance which is held there
        subgroup (obj, id): corresponding subgroup in the Cell
    Ordering by time coordinates aka dtp
    """
    group = models.ForeignKey('Group')
    dtp = models.ForeignKey('DayTimeParity')
    subject = models.ForeignKey('Subject')
    subgroup = models.ForeignKey('Subgroup')

    class Meta:
        ordering = ['dtp']


class ErrorMessage(models.Model):
    """Helping method to serialize error messages of API
    Fields:
        message (str): contents of the error
    """
    message = models.CharField(max_length=200)
