import json
import os
import datetime
import server_sniffer_utils.ansible_gatherer as ag
import server_sniffer_utils.mongo_helper as mh
from django.shortcuts import render
from more_itertools import chunked

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
DB_NAME = "server_sniffer"
INVENTORY_FILE = "inventory.yaml"

mongo_helper = mh.MongoHelper(DB_NAME, MONGO_HOST, MONGO_PORT)
ansible_gatherer = ag.AnsibleGatherer(INVENTORY_FILE)


# Create your views here.

def index(request):
    context = {}
    CHUNK_SIZE = 10
    
    server_names = ansible_gatherer.get_server_names()
    servers_names_chunks = list(chunked(server_names, CHUNK_SIZE))

    context['servers_names_chunks'] = servers_names_chunks
    context['page_title'] = 'Server Sniffer'
    
    return render(request, 'app/index.html', context)


def server_info(request, server_name):
    context = {}

    today_date = datetime.date.today()
    yesterday_date = today_date - datetime.timedelta(days=1)
    today_collection_name = mongo_helper.get_collection_name(today_date)
    yesterday_collection_name = mongo_helper.get_collection_name(yesterday_date)

    today_server_info = mongo_helper.find_document(today_collection_name, server_name)
    yesterday_server_info = mongo_helper.find_document(yesterday_collection_name, server_name)
    
    ddiff = mongo_helper.get_ddiff(yesterday_server_info, today_server_info)

    context['old_server_info'] = json.dumps(yesterday_server_info)
    context['new_server_info'] = json.dumps(ddiff)
    context['old_datetime'] = yesterday_collection_name
    context['new_datetime'] = today_collection_name
    context['page_title'] = server_name

    return render(request, 'app/server_info.html', context)


