#!/usr/bin/python3

import datetime
import os
from multiprocessing import Pool

import server_sniffer_utils.ansible_gatherer as ag
import server_sniffer_utils.mongo_helper as mh

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = int(os.environ.get("MONGO_PORT"))
DB_NAME = os.environ.get("DB_NAME")

INVENTORY_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
NUM_WORKING_PROCS = int(os.environ.get("NUM_WORKING_PROCS"))
ROTATION = int(os.environ.get("ROTATION"))

#MONGO_HOST="localhost"
#MONGO_PORT=27017
#DB_NAME="server_sniffer"
#NUM_WORKING_PROCS=10
#ROTATION=30


def main():
    mongo_helper = mh.MongoHelper(DB_NAME, MONGO_HOST, MONGO_PORT)

    collection_names = mongo_helper.get_collection_names()
    collection_dates = [mongo_helper.get_collection_date(col_name) for col_name in collection_names if col_name != DB_NAME]

    if len(collection_dates) > ROTATION:
        oldest_collection_date = min(collection_dates)
        mongo_helper.drop_collection(mongo_helper.get_collection_name(oldest_collection_date))

    today_collection_name = mongo_helper.get_collection_name(datetime.date.today())

    if (today_collection_name not in collection_names):
        mongo_helper.create_collection(today_collection_name)
    
    ansible_gatherer = ag.AnsibleGatherer(os.path.join(INVENTORY_FILE_DIR, "inventory.yaml"))

    documented_servers = mongo_helper.get_documents(today_collection_name)
    undocumented_servers = list(set(ansible_gatherer.get_server_names()) - set(documented_servers))

    with Pool(NUM_WORKING_PROCS) as p:
        docs = p.map(ansible_gatherer.gather_server_info, undocumented_servers)

    if docs:
        mongo_helper.insert_documents(today_collection_name, docs)


if __name__ == "__main__":
    main()
