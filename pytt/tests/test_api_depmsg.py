from django.test import TestCase
from pytt.models import Department
from rest_framework import status
import json

class TestDepartmentMessageGetAPI(TestCase):
    def setUp(self):
        Department(**{'name': 'Test Deparment',
                      'tag': 'td',
                      'dtype': '0',
                      'info': 'Hello. This is Test Department'
                      }).save()

    def test_correct_department_msg_request_response(self):
        expect = {'info': 'Hello. This is Test Department'}
        response = self.client.get('/3/departments/td/msg')
        response.render()
        assert json.loads(response.content) == expect

    def test_correct_department_msg_request_status(self):
        response = self.client.get('/3/departments/td/msg')
        assert response.status_code == status.HTTP_200_OK

    def test_incorrect_department_msg_request_response(self):
        expect = {'message': 'No such department'}
        response = self.client.get('/3/departments/incr/msg')
        response.render()
        assert json.loads(response.content) == expect

    def test_incorrect_department_msg_request_status(self):
        response = self.client.get('/3/departments/incr/msg')
        assert response.status_code == status.HTTP_404_NOT_FOUND
