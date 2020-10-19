from django.shortcuts import render

# Create your views here.
from check_es.models import Django_ES

from datetime import datetime
import pytz

def home(request):
    es_data = list(Django_ES.objects.all().order_by("pk").values())
    timestamp = es_data[0]['es_time']
    for i in es_data:
        i['es_name'] = str(i['es_name']).replace("_", " ")
    utc_time = timestamp.replace(tzinfo=pytz.utc)
    ist_time = utc_time.astimezone(pytz.timezone('Asia/Kolkata'))
    return render(request, 'check_es/home.html', context={'es_data':es_data, 'timestamp':ist_time})
