from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

# Create your views here.
@csrf_exempt
def index(request):
    images_list = []
    return HttpResponse(serializers.serialize("json", images_list))
