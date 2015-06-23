from django.test import TestCase
from pytt.models import *
from rest_framework import status
import json

class TestGroupTTGetAPI(TestCase):
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

    def test_correct_tt_request_response(self):
        expect = [
                    {
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
                            'teacher':{
                                'name':'Teacher',
                                'ssu_id':1
                            },
                            'activity':'lecture'
                        }
                    }
                 ]
        response = self.client.get('/3/departments/td/groups/251?gform=1&gtype=0')
        response.render()
        assert json.loads(response.content) == expect

    def test_correct_tt_request_response_implicit_type(self):
        expect = [
                    {
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
                            'teacher':{
                                'name':'Teacher',
                                'ssu_id':1
                            },
                            'activity':'lecture'
                        }
                    }
                 ]
        response = self.client.get('/3/departments/td/groups/251')
        response.render()
        assert json.loads(response.content) == expect

    def test_correct_tt_request_status(self):
        response = self.client.get('/3/departments/td/groups/251?gform=1&gtype=0')
        assert response.status_code == status.HTTP_200_OK

    def test_correct_tt_request_status_implicit(self):
        response = self.client.get('/3/departments/td/groups/251')
        assert response.status_code == status.HTTP_200_OK

    def test_no_group_tt_request_response_implicit(self):
        expect = {'message': 'No such group'}
        response = self.client.get('/3/departments/td/groups/5000')
        response.render()
        assert json.loads(response.content) == expect

    def test_no_group_tt_request_status_implicit(self):
        response = self.client.get('/3/departments/td/groups/5000')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_no_group_tt_request_response(self):
        expect = {'message': 'No such group'}
        response = self.client.get('/3/departments/td/groups/5000?gform=1&gtype=0')
        response.render()
        assert json.loads(response.content) == expect

    def test_no_group_tt_request_status(self):
        response = self.client.get('/3/departments/td/groups/5000?gform=1&gtype=0')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_no_dep_tt_request_response(self):
        expect = {'message': 'No such department'}
        response = self.client.get('/3/departments/incr/groups/251?gform=1&gtype=0')
        response.render()
        with open('f', 'w') as f:
            f.write(str(response.content))
        assert json.loads(response.content) == expect

    def test_no_dep_tt_request_status(self):
        response = self.client.get('/3/departments/incr/groups/5000?gform=1&gtype=0')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_mul_grp_tt_request_response(self):
        expect = {'message': 'Multiple groups returned'}
        response = self.client.get('/3/departments/td/groups/151')
        response.render()
        assert json.loads(response.content) == expect

    def test_mul_grp_tt_request_status(self):
        response = self.client.get('/3/departments/td/groups/151')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_grp_tt_request_response(self):
        expect = {'message': 'No timetable for this group'}
        response = self.client.get('/3/departments/td/groups/151?gform=1&gtype=0')
        assert json.loads(response.content) == expect

    def test_empty_grp_tt_request_status(self):
        response = self.client.get('/3/departments/td/groups/151?gform=1&gtype=0')
        assert response.status_code == status.HTTP_205_RESET_CONTENT



