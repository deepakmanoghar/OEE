from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Machine, ProductionLog
from .serializers import MachineSerializer, ProductionLogSerializer

class MachineTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.machine_data = {'machine_name': 'Machine 1', 'machine_serial_no': 'SN001'}
        self.response = self.client.post('/machines/', self.machine_data, format='json')

    def test_machine_creation(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_machine_get(self):
        machine = Machine.objects.get()
        response = self.client.get(f'/machines/{machine.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)