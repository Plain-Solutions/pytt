from django.test import TestCase
from pytt.models import TimeReference
from rest_framework import status
import json

class TestTimeReferenceGetAPI(TestCase):
    def setUp(self):
        times = [('08:20', '09:50'),
                      ('10:00', '11:35')]
        TimeReference(**{'dtype': 0,
                         'sequence': 0,
                         'begin':times[0][0],
                         'end': times[0][1]}).save()

        TimeReference(**{'dtype': 0,
                         'sequence': 1,
                         'begin':times[1][0],
                         'end': times[1][1]}).save()


    def test_tr_request_response(self):
        expect = [
                    {
                        'dtype':0,
                        'times':[
                            {
                                'sequence':0,
                                'begin':'08:20',
                                'end':'09:50'
                            },
                            {
                                'sequence':1,
                                'begin':'10:00',
                                'end':'11:35'
                            }
                        ]
                    }
                 ]
        response = self.client.get('/3/times')
        response.render()
        assert json.loads(response.content) == expect

    def test_tr_request_status(self):
        response = self.client.get('/3/times')
        assert response.status_code == status.HTTP_200_OK
