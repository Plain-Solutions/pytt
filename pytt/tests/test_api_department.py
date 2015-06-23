from django.test import TestCase
from pytt.models import Department
from rest_framework import status
import json

class TestDepartmentGetAPI(TestCase):
    def setUp(self):
        Department(**{'name': 'Test Department',
                      'tag': 'td',
                      'dtype': 0,
                      'info': 'Hello. This is Test Department'
                      }).save()


    def test_correct_department_request_response(self):
        expect = [{'name': 'Test Department',
                  'tag': 'td',
                  'dtype': 0
                  }]
        response = self.client.get('/3/departments')
        response.render()
        assert json.loads(response.content) == expect

    def test_correct_department_request_status(self):
        response = self.client.get('/3/departments')
        assert response.status_code == status.HTTP_200_OK
