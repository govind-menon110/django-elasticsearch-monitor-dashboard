from django.db import models
from datetime import datetime 

class Django_ES(models.Model):
    es_id = models.IntegerField(primary_key=True)
    es_name = models.CharField(max_length=1000)
    es_url = models.CharField(max_length=2000)
    kibana_url = models.CharField(max_length=4500)
    kibana_filter = models.CharField(max_length=4500)
    desc = models.CharField(max_length=2000)
    es_health = models.CharField(max_length=10)
    es_query = models.CharField(max_length=1500)
    es_json_docs = models.IntegerField()
    doc_color = models.CharField(max_length=10)
    es_time = models.DateTimeField()
