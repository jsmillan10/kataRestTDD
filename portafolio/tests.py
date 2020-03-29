from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.http import JsonResponse

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
        response=self.client.post('/portafolio/addUser/',json.dumps({"username": "testUser", "first_name": "Test", "last_name": "User", "password": "AnyPas#5", "email": "test@test.com"}), content_type='application/json')
        current_data=json.loads(response.content)
        self.assertEqual(current_data[0]['fields']['username'],'testUser')

    def test_count_portafolio_public_list(self):
        user_model = User.objects.create_user(username='test', password='kd8wke-DE34', first_name='test',
                                              last_name='test', email='test@test.com')
        Portafolio.objects.create(name='nuevo', url='No', description='testImage', public=False, type='jpg', user=user_model)
        Portafolio.objects.create(name='nuevo2', url='No', description='testImage', type='jpg', user=user_model)
        Portafolio.objects.create(name='nuevo3', url='No', description='testImage', public=False, type='jpg', user=user_model)
        Portafolio.objects.create(name='nuevo4', url='No', description='testImage', type='jpg', user=user_model)
        Portafolio.objects.create(name='nuevo5', url='No', description='testImage', public=True, type='jpg',
                                  user=user_model)
        response = self.client.get('/portafolio/')
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data), 3)

    def test_login_user(self):
        self.client.post('/portafolio/addUser/', json.dumps(
            {"username": "testUser", "first_name": "Test", "last_name": "User", "password": "AnyPas#5",
             "email": "test@test.com"}), content_type='application/json')
        response=self.client.post('/portafolio/login/',json.dumps({"username": "testUser", "password": "AnyPas#5"}), content_type='application/json')
        current_data=json.loads(response.content)
        self.assertEqual(current_data['message'],'Login Exitoso')

    def test_fail_login_user(self):
        self.client.post('/portafolio/addUser/', json.dumps(
            {"username": "testUser", "first_name": "Test", "last_name": "User", "password": "AnyPas#5",
             "email": "test@test.com"}), content_type='application/json')
        response=self.client.post('/portafolio/login/',json.dumps({"username": "testUser", "password": "AnyPas#6"}), content_type='application/json')
        current_data=json.loads(response.content)
        self.assertEqual(current_data['message'],'Login Fallido')

    def test_update_user(self):
        self.client.post('/portafolio/addUser/', json.dumps(
            {"username": "testUser", "first_name": "Test", "last_name": "User", "password": "AnyPas#5",
             "email": "test@test.com"}), content_type='application/json')
        response = self.client.post('/portafolio/updateUser/', json.dumps({"username": "testUser", "first_name": "TestUpdate", "last_name": "TestUpdate2"}),
                                    content_type='application/json')
        current_data = json.loads(response.content)
        self.assertEqual(current_data['first_name'],'TestUpdate')
        self.assertEqual(current_data['last_name'],'TestUpdate2')

    def test_update_public_mark(self):
        user_model = User.objects.create_user(username='test', password='kd8wke-DE34', first_name='test',
                                              last_name='test', email='test@test.com')
        Portafolio.objects.create(name='nuevo1', url='No', description='testImage', type='jpg', user=user_model)
        Portafolio.objects.create(name='nuevo2', url='No', description='testImage', type='jpg', public=False, user=user_model)
        Portafolio.objects.create(name='nuevo3', url='No', description='testImage', type='jpg', public=False, user=user_model)
        Portafolio.objects.create(name='nuevo4', url='No', description='testImage', type='jpg', public=False,
                                  user=user_model)
        response = self.client.post('/portafolio/updatePermission/', json.dumps([{"name":"nuevo1","public":False},{"name": "nuevo4", "public": True}]), content_type='application/json')
        current_data = json.loads(response.content)
        self.assertEqual(current_data[0]['name'], 'nuevo1')
        self.assertEqual(current_data[0]['public'], False)
        self.assertEqual(current_data[1]['name'], 'nuevo4')
        self.assertEqual(current_data[1]['public'], True)

    def test_add_image(self):
        user_model = User.objects.create_user(username='test', password='kd8wke-DE34', first_name='test', last_name='test', email='test@test.com')
        Portafolio.objects.create(name='nuevo1', url='No', description='testImage', type='jpg', user=user_model)
        Portafolio.objects.create(name='nuevo2', url='No', description='testImage', type='jpg', public=False, user=user_model)
        response = self.client.post('/portafolio/addImage/', json.dumps({"name":'nuevo3', "url":'No', "description":'testImage', "type":'jpg', "username":"test"}), content_type='application/json')
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data),3)