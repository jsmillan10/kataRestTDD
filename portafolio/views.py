from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import Portafolio
from django.contrib.auth import authenticate, login, logout
import json


# Create your views here.
@csrf_exempt
def index(request):
    images_list = Portafolio.objects.filter(public=True)
    return HttpResponse(serializers.serialize("json", images_list))


@csrf_exempt
def add_user_view(request):
    if request.method == 'POST':
        json_user = json.loads(request.body)
        username = json_user['username']
        first_name = json_user['first_name']
        last_name = json_user['last_name']
        password = json_user['password']
        email = json_user['email']

        user_model = User.objects.create_user(username=username, password=password)
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.email = email
        user_model.save()
    return HttpResponse(serializers.serialize("json", [user_model]))


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        jsonUser = json.loads(request.body)
        username = jsonUser['username']
        password = jsonUser['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            message = "Login Exitoso"
        else:
            message = 'Login Fallido'
    return JsonResponse({"message": message})


@csrf_exempt
def update_user(request):
    if request.method == 'POST':
        jsonUser = json.loads(request.body)
        username = jsonUser['username']
        firstName = jsonUser['first_name']
        lastName = jsonUser['last_name']
        User.objects.filter(username=username).update(first_name=firstName, last_name=lastName)
    return JsonResponse({"first_name": firstName, 'last_name': lastName})


@csrf_exempt
def update_permission_user(request):
    if request.method == 'POST':
        jsonData = json.loads(request.body)
        result = []
        for porta in list(jsonData):
            paso = Portafolio.objects.filter(name=porta['name']).update(public=porta['public'])
            if paso == 1:
                result.append(porta)
    return JsonResponse(result, safe=False)


@csrf_exempt
def add_portafolio(request):
    if request.method == 'POST':
        json_image = json.loads(request.body)
        name = json_image['name']
        url = json_image['url']
        description = json_image['description']
        tipo = json_image['type']
        public = json_image['public']
        username = json_image['username']
        user_model = User.objects.get(username=username)
        Portafolio.objects.create(name=name, url=url, description=description, type=tipo, public=public,
                                  user=user_model)
        images = Portafolio.objects.all()
    return HttpResponse(serializers.serialize("json", images))
