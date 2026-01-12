from django.test import TestCase
from django.urls import reverse
from .models import Station, Threshold
from .utils import get_station_status

class UtilsTests(TestCase):
    def test_get_station_status_wrong(self):
        t = Threshold(limit_value=10, status_type='WRONG')
        self.assertEqual(get_station_status(15, [t]), 'WRONG')

    def test_get_station_status_right(self):
        t = Threshold(limit_value=100, status_type='WRONG')
        self.assertEqual(get_station_status(15, [t]), 'RIGHT')

class ViewsTests(TestCase):
    def test_dashboard_shows_station_status(self):
        s = Station.objects.create(name='S1', current_value=50)
        Threshold.objects.create(station=s, limit_value=10, status_type='WRONG')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        stations = response.context['stations']
        self.assertTrue(any(st['name'] == 'S1' and st['status'] == 'WRONG' for st in stations))
