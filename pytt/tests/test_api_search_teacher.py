from django.test import TestCase
from pytt.models import Teacher
from rest_framework import status
import json

class TestTeacherSearchAPI(TestCase):
    def setUp(self):
        teacher = Teacher(**{'ssu_id': 1,
                             'name': 'Teacher'})
        teacher.save()
        teacher2 = Teacher(**{'ssu_id': 2,
                              'name': 'Guy'})
        teacher2.save()

    def test_correct_search_request_response(self):
        expect = [{'ssu_id': 1, 'name': 'Teacher'}]
        response = self.client.get('/3/teachers?name=Teacher')
        response.render()
        assert json.loads(response.content) == expect

    def test_correct_search_request_status(self):
        response = self.client.get('/3/teachers?name=Teacher')
        assert response.status_code == status.HTTP_200_OK

    def test_nonexist_search_request_response(self):
        expect = {'message': 'No matching names found'}
        response = self.client.get('/3/teachers?name=Nosuch')
        response.render()
        assert json.loads(response.content) == expect

    def test_nonexist_search_request_status(self):
        response = self.client.get('/3/teachers?name=Nosuch')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_all_search_request_response(self):
        expect = [
                    {
                        "name":"Guy",
                        "ssu_id":2
                    },
                    {
                        "name":"Teacher",
                        "ssu_id":1
                    }
                 ]
        response = self.client.get('/3/teachers?name=all')
        response.render()
        assert json.loads(response.content) == expect

    def test_all_search_request_status(self):
        response = self.client.get('/3/teachers?name=all')
        assert response.status_code == status.HTTP_200_OK

    def test_incor_search_request_response(self):
        expect = {'message': 'This request is only possible with either \'name\' or\
 \'name=all\' parameters'}
        response = self.client.get('/3/teachers')
        response.render()
        assert json.loads(response.content) == expect

    def test_incor_search_request_status(self):
        response = self.client.get('/3/teachers')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

