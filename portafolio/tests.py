from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from .models import Image
import json


def test_list_portafolio_status(self):
    url = '/gallery/'
    response = self.client.get(url, format='json')
    self.assertEqual(response.status_code, 200)