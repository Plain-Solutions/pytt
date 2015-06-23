from django.test import TestCase
from pytt.models import Department, Group
from rest_framework import status
import json

class TestGroupGetAPI(TestCase):
    def setUp(self):
        dp = Department(**{'name': 'Test Deparment',
                           'tag': 'td',
                           'dtype': '0',
                           'info': 'Hello. This is Test Department'
                          })
        dp.save()
        Department(**{'name': 'Empty Deparment',
                      'tag': 'ed',
                      'dtype': '0',
                      'info': 'Hello. This is department with no groups'
                      }).save()
        Group(**{'department': dp,
                 'name': '251',
                 'gtype': 0,
                 'gform': 1
                 }).save()

    def test_correct_group_request_response(self):
        expect = [{'name': '251',
                   'gtype': 0,
                   'gform': 1
                  }]
        response = self.client.get('/3/departments/td/groups')
        response.render()
        assert json.loads(response.content) == expect

    def test_correct_group_request_status(self):
        response = self.client.get('/3/departments/td/groups')
        assert response.status_code == status.HTTP_200_OK

    def test_empty_group_request_response(self):
        response = self.client.get('/3/departments/ed/groups')
        response.render()
        assert json.loads(response.content) == []

    def test_empty_group_request_status(self):
        response = self.client.get('/3/departments/ed/groups')
        assert response.status_code == status.HTTP_200_OK

    def test_incor_dep_group_request_response(self):
        expect = {'message': 'No such department'}
        response = self.client.get('/3/departments/incor/groups')
        response.render()
        assert json.loads(response.content) == expect

    def test_incor_dep_group_request_status(self):
        response = self.client.get('/3/departments/incor/groups')
        assert response.status_code == status.HTTP_404_NOT_FOUND
