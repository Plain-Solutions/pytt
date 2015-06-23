from django.test import TestCase
from pytt.models import *
from rest_framework import status
import json

class TestTeacherTTGetAPI(TestCase):
    def setUp(self):
        dp = Department(**{'name': 'Test Department',
                           'tag': 'td',
                           'dtype': 0,
                           'info': 'Hello. This is Test Department'
                          })
        dp.save()
        grp = Group(**{'department': dp,
                       'name': '251',
                       'gtype': 0,
                       'gform': 1
                      })
        grp2 = Group(**{'department': dp,
                        'name': '151',
                        'gtype': 0,
                        'gform': 1
                       })
        grp3 = Group(**{'department': dp,
                        'name': '151',
                        'gtype': 0,
                        'gform': 0})
        grp.save()
        grp2.save()
        grp3.save()

        cell = Cell()

        dtp = DayTimeParity(**{'day': 0,
                               'time': 0,
                               'parity': 'even'
                               })
        dtp.save()

        teacher = Teacher(**{'ssu_id': 1,
                             'name': 'Teacher'})
        teacher.save()

        Teacher(**{'ssu_id': 2,
                   'name': 'Guy'}).save()
        Teacher(**{'ssu_id': 3,
                   'name': 'Some Guy'}).save()
        Teacher(**{'ssu_id': 3,
                   'name': 'Some Incor Guy'}).save()

        subj = Subject(**{'name': 'Python',
                          'begin_date': 0,
                          'end_date': 0})
        subj.save()

        subgroup = Subgroup(**{'name': 'g1',
                               'location': 'Loc',
                               'teacher': teacher,
                               'activity': 'lecture'
                               })
        subgroup.save()
        cell.group = grp
        cell.dtp = dtp
        cell.subject = subj
        cell.subgroup = subgroup
        cell.save()

    def test_correct_ttt_request_response(self):
        expect = [
                    {
                        'group':{
                            'department':{
                                'tag':'td'
                            },
                            'name':'251',
                            'gform':1,
                            'gtype':0
                        },
                        'dtp':{
                            'day':0,
                            'time':0,
                            'parity':'even'
                        },
                        'subject':{
                            'name':'Python',
                            'begin_date':0,
                            'end_date':0
                        },
                        'subgroup':{
                            'name':'g1',
                            'location':'Loc',
                            'activity':'lecture'
                        }
                    }
                 ]
        response = self.client.get('/3/teachers/1')
        response.render()
        assert json.loads(response.content) == expect

    def test_correct_ttt_request_status(self):
        response = self.client.get('/3/teachers/1')
        assert response.status_code == status.HTTP_200_OK

    def test_empty_ttt_request_response(self):
        expect = {'message': 'No timtable for teacher with such ID'}
        response = self.client.get('/3/teachers/2')
        response.render()
        assert json.loads(response.content) == expect

    def test_empty_ttt_request_status(self):
        response = self.client.get('/3/teachers/2')
        assert response.status_code == status.HTTP_412_PRECONDITION_FAILED

    def test_no_teacher_ttt_request_response(self):
        expect = {'message': 'Teacher with such ID doesn\'t exists'}
        response = self.client.get('/3/teachers/12345')
        response.render()
        assert json.loads(response.content) == expect

    def test_no_teacher_ttt_request_status(self):
        response = self.client.get('/3/teachers/12345')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_mul_teacher_ttt_request_response(self):
        expect = {'message': 'More than one teacher with such ID returned. Please report about\
 this issue to developers ASAP'}
        response = self.client.get('/3/teachers/3')
        response.render()
        assert json.loads(response.content) == expect

    def test_mul_teacher_ttt_request_status(self):
        response = self.client.get('/3/teachers/3')
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
