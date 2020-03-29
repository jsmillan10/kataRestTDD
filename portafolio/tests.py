from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from .models import Portafolio
import json

class PortafolioTestCase(TestCase):
    def test_list_portafolio_status(self):
        url = '/portafolio/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_count_portafolio_list(self):
        user_model = User.objects.create_user(username='test', password='kd8wke-DE34', first_name='test',
                                              last_name='test', email='test@test.com')
        Portafolio.objects.create(name='nuevo', url='No', description='testImage', type='jpg', user=user_model)
        Portafolio.objects.create(name='nuevo2', url='No', description='testImage', type='jpg', user=user_model)
        Portafolio.objects.create(name='nuevo3', url='No', description='testImage', type='jpg', user=user_model)
        Portafolio.objects.create(name='nuevo4', url='No', description='testImage', type='jpg', user=user_model)

        response = self.client.get('/portafolio/')
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data), 4)

    def test_add_user(self):
        response=self.client.post('/gallery/addUser/',json.dumps({"username": "testUser", "first_name": "Test", "last_name": "User", "password": "AnyPas#5", "email": "test@test.com"}), content_type='application/json')
        current_data=json.loads(response.content)
        self.assertEqual(current_data[0]['fields']['username'],'testUser')