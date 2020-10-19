import requests
from check_es.models import Django_ES
from datetime import datetime
import pytz
import threading
import json

def get_es_health(es_url):
    health_endpoint = '/_cluster/health'

    try:
        r = requests.get(es_url + health_endpoint, timeout=2)
        r.raise_for_status()
        return r.json()
    except Exception as em:
        with open('errors.log', 'a') as errorfile:
            errorfile.write("EXCEPTION: " + str(em))
        return None
    except requests.RequestException:
        return None
    except requests.Timeout:
        return None

def get_es_docs(es_url, index, time):
    try:
        query = json.dumps({
                "query": 
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "now-"+str(time)
                            }              
                        }
                    },
                "size":0, 
                "track_total_hits":'true'
        })   
        response = requests.get(str(es_url)+str(index), data=query, headers={'content-type': 'application/json'}, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as em:
        with open('errors.log', 'a') as errorfile:
            errorfile.write("EXCEPTION: " + str(em))
        return None
    except requests.RequestException:
        return None
    except requests.Timeout:
        return None



def update_db():
    #input the file
    #File has id, es_name, es_url, kibana_url, query_index, doc_limit, es_desc
    IST = pytz.timezone('Asia/Kolkata')
    with open('config.json','r') as es_file:
        es_loaded = json.loads(es_file.read())
        print(es_loaded)
    for i in es_loaded:
        # with open('errors.log', 'a') as errors:
        #     errors.write("splitstring is: " + str(splitstr) + " \n")
        if (i['query_index']=="x"):
            try:
                new_es = Django_ES()
                name_of_es = i['es_name']
                new_es.es_id = i['id']
                new_es.desc = i['es_desc']
                new_es.kibana_url = i['kibana_url']
                new_es.es_url = i['es_url']
                new_es.es_query = i['query_index']
                new_es.es_json_docs = 0
                json_limit = i['doc_limit']
                new_es.doc_color = "white"
                if (i['kibana_filter']=="x"):
                    new_es.kibana_filter = i['kibana_url']
                else:
                    new_es.kibana_filter = i['kibana_filter']
                new_es.es_name = name_of_es
                new_es.es_health = "white"
                timeutc = datetime.utcnow().replace(tzinfo=pytz.utc)
                new_es.es_time = timeutc.astimezone(pytz.timezone('Asia/Kolkata'))
                #        with open('errors.log', 'a') as errors:
                #        errors.write("es is: " + str(new_es) + " \n")
                new_es.save()
                continue
            except Exception as em:
                with open('errors.log', 'a') as errorfile:
                    errorfile.write("EXCEPTION: " + str(em) + " \n")
                continue
        json_url = get_es_health(i['es_url'])
        json_docs = get_es_docs(i['es_url'],i['query_index'], "30m")
        doc_value = get_es_docs(i['es_url'],i['query_index'], "12h")
        if json_docs is not None:
            json_docs = json_docs["hits"]["total"]["value"]
        else:
            json_docs = 0
        if doc_value is not None:
            doc_value = doc_value["hits"]["total"]["value"]
        else:
            doc_value = 0
        if json_url is not None:
            try:
                new_es = Django_ES()
                name_of_es = i['es_name']
                new_es.es_id = i['id']
                new_es.desc = i['es_desc']
                new_es.kibana_url = i['kibana_url']
                new_es.es_url = i['es_url']
                new_es.es_query = i['query_index']
                new_es.es_json_docs = doc_value
                json_limit = i['doc_limit']
                if int(json_docs) < int(json_limit):
                    new_es.doc_color = "red"
                else:
                    new_es.doc_color = "green"
                new_es.kibana_filter = i['kibana_filter']
                new_es.es_name = name_of_es
                new_es.es_health = json_url['status']
                timeutc = datetime.utcnow().replace(tzinfo=pytz.utc)
                new_es.es_time = timeutc.astimezone(pytz.timezone('Asia/Kolkata'))
                #        with open('errors.log', 'a') as errors:
                #        errors.write("es is: " + str(new_es) + " \n")
                new_es.save()
            except Exception as em:
                with open('errors.log', 'a') as errorfile:
                    errorfile.write("EXCEPTION: " + str(em) + " \n")
                pass
        else:
            try:
                new_es = Django_ES()
                name_of_es = i['es_name']
                new_es.es_id = i['id']
                new_es.desc = i['es_desc']
                new_es.kibana_url = i['kibana_url']
                new_es.es_url = i['es_url']
                new_es.es_query = i['query_index']
                new_es.es_json_docs = doc_value
                json_limit = i['doc_limit']
                if int(json_docs) < int(json_limit):
                    new_es.doc_color = "red"
                else:
                    new_es.doc_color = "green"
                new_es.kibana_filter = i['kibana_filter']
                new_es.es_name = name_of_es
                new_es.es_health = "red"
                timeutc = datetime.utcnow().replace(tzinfo=pytz.utc)
                new_es.es_time = timeutc.astimezone(pytz.timezone('Asia/Kolkata'))
        #        with open('errors.log', 'a') as errors:
        #            errors.write("es is: " + str(new_es) + " \n")
                new_es.save()
            except Exception as em:
                with open('errors.log', 'a') as errorfile:
                    errorfile.write("EXCEPTION: " + str(em) + " \n")
                pass
    timer = threading.Timer(40, update_db)
    timer.start()
