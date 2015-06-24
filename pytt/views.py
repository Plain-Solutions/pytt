# -*- coding: utf-8 -*-
"""Module, containing all the view methods"""

from pytt.models import *
from pytt.serializers import DepartmentSerializer, DepartmentMessageSerializer
from pytt.serializers import GroupSerializer, ErrorSerializer, CellSerializer
from pytt.serializers import TeacherSerializer, TeacherCellSerializer
from pytt.serializers import TRSerializer, PRSerializer, FullPRSerializer

from django.conf import settings
from django.views.decorators.cache import cache_page

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import HTMLParser
import copy
import datetime

"""Messages to send to user"""

NO_DEP_MSG = 'No such department'
NO_GRP_MSG = 'No such group'
MUL_GRP_MSG = 'Multiple groups returned'
MIS_PRM_MSG = 'This request is only possible with either \'name\' or\
 \'name=all\' parameters'
NO_MATCH_MSG = 'No matching names found'
NO_TC_MSG = 'Teacher with such ID doesn\'t exists'
MANY_TC_MSG = 'More than one teacher with such ID returned. Please report about\
 this issue to developers ASAP'
NO_GTT_MSG = 'No timetable for this group'
NO_TTT_MSG = 'No timtable for teacher with such ID'
INCOR_INC_MSG = 'Input date is incorrect and/or doesn\'t match YYYY-MM-DD'
NO_DATE_MSG = 'No date was found'
NO_DATE_TODAY_MSG = 'Today date wasn\'t found in the database, something went\
 horribly wrong. Please report about this issue to developers ASAP'
NO_DATE_AT_ALL_MSG = 'No dates were found in the database, something went\
 horribly wrong. Please report about this issue to developers ASAP'
MUL_DATE_MSG = 'More than one parity for the date returned, something went\
 horribly wrong. Please report about this issue to developers ASAP'


@api_view(['GET'])
@cache_page(settings.UPDATE_INTERVAL)
def list_tr(request):
    """ List all the available timereferences. View with simplest
    information: returns times of classes in their time order
    organized by dtype.
    Possible statuses:
        200 - OK
    Example answer:
    [
        { dtype: 1,
          times: [ { sequence: 0,
                     begin: '08:20',
                     end: '09:50' },
                     ...
                 ]
        },
        ...
    ]

    """
    data = TimeReference.objects.all()
    return Response([{'dtype': x,
                      'times': [TRSerializer(z).data \
                                for z in data if z.dtype == x]} \
                      for x in list(set([y.dtype for y in data]))])

@api_view(['GET'])
@cache_page(settings.UPDATE_INTERVAL)
def list_departments(request):
    """List departments names, tags and dtypes.
    Possible statuses:
        200 - OK
    Exmaple answer:
    [
        ...,
        {
            "name": "CSIT",
            "tag": "knt",
            "dtype": 1
        },
        ...
    ]
    """
    return Response(DepartmentSerializer(Department.objects.all(),
                                         many=True).data)


@api_view(['GET'])
@cache_page(settings.UPDATE_INTERVAL)
def get_department_msg(request, deptag):
    """Get department message (message) for specific departments
    Parameter:
        deptag: tag of department
    Possible statuses:
        200 - OK
        404 - Requested department does not exists
    Example answer in case of OK:
    {
        "info":  "Some crucial info here!"
    }
    Example answer in case of failure:
    {
        "message": "No such department"
    }
    """
    try:
        return Response(DepartmentMessageSerializer(
                        Department.objects.get(tag=deptag)
                        ).data)
    except Department.DoesNotExist:
        return Response(ErrorSerializer(ErrorMessage(message=NO_DEP_MSG)).data,
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@cache_page(settings.UPDATE_INTERVAL)
def get_department_groups(request, deptag):
    """ Get group list with names and gtypes/gforms for specific department
    Parameter:
        deptag: tag of department
    Possible statuses:
        200 - OK
        404 - Requested department does not exists
    Example answer in case of OK:
    [
        {
            "name": "111",
            "gform": 0,
            "gtype": 1
        },
        {
            "name": "131",
            "gform": 0,
            "gtype": 0
        },
        ...
    ]
    Example answer in case of failure equals the previous request:
    {
        "message": "No such department"
    }
    """
    try:
        return Response(GroupSerializer(
                        Group.
                        objects
                        .filter(department=Department.objects.get(tag=deptag)),
                                many=True).data)
    except Department.DoesNotExist:
        return Response(ErrorSerializer(ErrorMessage(message=NO_DEP_MSG)).data,
                        status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@cache_page(settings.UPDATE_INTERVAL)
def get_timetable(request, deptag, groupname):
    """ Get timetable for specific group
    Parameters:
        deptag: tag of department
        groupname: name of the group supplied by optional ?gtype=X&gform=X
    If groupname passed without optional classifiers, server will try
    to cast it to existing group in department with such name. If multiple
    groups with the same names (e.g., full-time and evening) exists, then
    MulipleObjectsReturned exception is thrown.
    Possible statuses:
        200 - OK
        404 - Requested department or group does not exists
        205 - No timetable for this group
        400 - Malformed request (multiple groups matching found)
    Example 200 OK:
    [
        {
            "dtp": {
                "day": 0,
                "time": 0,
                "parity": "full"
            },
            "subject": {
                "name": "Объектно-ориентированное программирование",
                "begin_date": 0,
                "end_date": 0
            },
            "subgroup": {
                "name": "1 под.",
                "location": "12корпус ауд.416Б",
                "teacher": {
                    "name": "Батраева Инна Александровна",
                    "ssu_id": 132
                },
                "activity": "practice"
            }
        },
        ...
    ]
    Example 404 "doesn't exists"
    {
        "message": "No such department"
    }
    {
        "message": "No such group"
    }
    Example 205
    {
        "message": "No timetable for this group"
    }
    Example 400
    {
        "message": "Multiple groups returned"
    }
    """
    group = None
    try:
        try:
            Department.objects.get(tag=deptag)
            group = Group.objects.get(department__tag=deptag,
                                      name=groupname,
                                      gform=request.GET['gform'],
                                      gtype=request.GET['gtype'])
        except KeyError:
            group = Group.objects.get(department__tag=deptag,
                                      name=groupname)
    except Department.DoesNotExist:
        return Response(ErrorSerializer(ErrorMessage(message=NO_DEP_MSG)).data,
                        status=status.HTTP_404_NOT_FOUND)
    except Group.DoesNotExist:
        return Response(ErrorSerializer(
                        ErrorMessage(message=NO_GRP_MSG)).data,
                        status=status.HTTP_404_NOT_FOUND)
    except Group.MultipleObjectsReturned:
        return Response(ErrorSerializer(
                        ErrorMessage(message=MUL_GRP_MSG)).data,
                        status=status.HTTP_400_BAD_REQUEST)

    cells = Cell.objects.filter(group=group)
    if not len(cells):
        return Response(ErrorSerializer(
                        ErrorMessage(message=NO_GTT_MSG)).data,
                        status=status.HTTP_205_RESET_CONTENT)

    return Response(CellSerializer(cells, many=True).data)

@api_view(['GET'])
@cache_page(settings.UPDATE_INTERVAL)
def get_teacher_timetable(request, teacher_id):
    """Get teacher timetable
    Parameteres:
        teacher_id: ssu_id to get timetable for
    Possible statuses:
        200 - OK
        205 - No timetable for this teacher
        404 - Teacher doesn't exists
        500 - Multiple teachers for one ID. Internal error
    Example for 200:
    [
        {
            "group": {
                "department": {
                    "tag": "knt"
                },
                "name": "211",
                "gform": 0,
                "gtype": 1
            },
            "dtp": {
                "day": 0,
                "time": 1,
                "parity": "full"
            },
            "subject": {
                "name": "Теория автоматов и формальных языков",
                "begin_date": 0,
                "end_date": 0
            },
            "subgroup": {
                "name": "",
                "location": "12корпус ауд.312",
                "activity": "practice"
            }
        },
        ...
    ]
    Example for 412
    {
        "message": "No timetable for teacher with such ID"
    }
    Example for 404
    {
        "message": "Teacher with sud ID doesn't exists"
    }
    Example for 500 is in MANY_TC_MSG
    """
    try:
        Teacher.objects.get(ssu_id=teacher_id)
        cells = Cell.objects.filter(subgroup__teacher__ssu_id=teacher_id)
        if not len(cells):
            return Response(ErrorSerializer(ErrorMessage(message=NO_TTT_MSG))
                            .data,
                            status=status.HTTP_412_PRECONDITION_FAILED)
        return Response(TeacherCellSerializer(cells, many=True).data)
    except Teacher.DoesNotExist:
        return Response(ErrorSerializer(ErrorMessage(message=NO_TC_MSG)).data,
                        status=status.HTTP_404_NOT_FOUND)
    except Teacher.MultipleObjectsReturned:
        return Response(ErrorSerializer(ErrorMessage(message=MANY_TC_MSG))
                        .data,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@cache_page(settings.UPDATE_INTERVAL)
def search_teacher(request):
    """Search teacher by substring, return their id and matched names
    Parameters:
        passed by ?name: substring with name  or 'all' - to get all teacehrs
    Possible statuses:
        200 - OK
        404 - No such teacher (response in NO_MATCH_MSG)
        400 - Incorrect request (missing ?name) (response in MIS_PRM_MSG)
    Example for 200:
    [
        {
            "name": "Самойлов Виктор Геннадиевич",
            "ssu_id": 2942
        },
        ...
    ]
    """
    try:
        parser = HTMLParser.HTMLParser()
        matched_teachers = []
        if request.GET['name'] == 'all':
            matched_teachers = Teacher.objects.all()
        else:
            teacher_name = parser.unescape(request.GET['name'])
            matched_teachers = Teacher.objects.filter(
                name__contains=teacher_name)
        if not len(matched_teachers):
            return Response(ErrorSerializer(
                            ErrorMessage(message=NO_MATCH_MSG)).data,
                            status=status.HTTP_404_NOT_FOUND)
        return Response(TeacherSerializer(matched_teachers,
                                          many=True).data)
    except KeyError:
        return Response(ErrorSerializer(
                        ErrorMessage(message=MIS_PRM_MSG)).data,
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@cache_page(settings.UPDATE_INTERVAL)
def get_parity(request):
    """ Get current parity (automatically calculated)
    Params:
        ?day=: if none -> today, today -> today, all -> enlist all the DB
    records. Otherwise please give day in format YYYY-MM-DD.
    Possible statuses:
        200 - OK
        500 - No date for today found in DB. That's internal error, response
    example in NO_DATE_TODAY_MSG. In case day=all -> NO_DATE_AT_ALL_MSG.
    In case day=YYYY-MM-DD -> MUL_DATE_MSG (numerous parities for one day
    is an server error)
        400 - in case day=YYYY-MM-DD - date malformed or reference doesn't
    exists (yet) for this day
    Exaple for 200 OK (?day absent or day=today):
    {
        "is_even": false
    }
    ?day=all
    [
        {
            "begin_day": "2014-09-01",
            "end_day": "2014-09-07",
            "is_even": true
        },
        {
            "begin_day": "2014-09-08",
            "end_day": "2014-09-14",
            "is_even": false
        },
        ...
    ]
    ?day=2015-06-01
    {
        "is_even": false
    }
    """
    if 'day' not in request.GET or request.GET['day'] == 'today':
        try:
            return Response(PRSerializer(
                            ParityReference
                            .objects
                            .get(begin_day__lte=datetime.date.today(),
                                 end_day__gte=datetime.date.today())
                            ).data)
        except ParityReference.DoesNotExist:
            return Response(ErrorSerializer(
                            ErrorMessage(message=NO_DATE_TODAY_MSG)).data,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.GET['day'] == 'all':
        data = ParityReference.objects.all()
        if not len(data):
            return Response(ErrorSerializer(
                            ErrorMessage(message=NO_DATE_AT_ALL_MSG)).data,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(FullPRSerializer(data, many=True).data)
    elif 'day' in request.GET:
        try:
            check = datetime.datetime.strptime(request.GET['day'], '%Y-%m-%d')
            return Response(PRSerializer(
                            ParityReference
                            .objects
                            .get(begin_day__lte=check,
                                 end_day__gte=check)
                            ).data)
        except ValueError:
            return Response(ErrorSerializer(
                            ErrorMessage(message=INCOR_INC_MSG)).data,
                            status=status.HTTP_400_BAD_REQUEST)
        except ParityReference.DoesNotExist:
            return Response(ErrorSerializer(
                            ErrorMessage(message=NO_DATE_MSG)).data,
                            status=status.HTTP_400_BAD_REQUEST)
        except ParityReference.MultipleObjectsReturned:
            return Response(ErrorSerializer(
                            ErrorMessage(message=MUL_DATE_MSG)).data,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
