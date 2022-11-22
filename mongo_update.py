#!/usr/bin/python3

import datetime
import os
from multiprocessing import Pool

import server_sniffer_utils.ansible_gatherer as ag
import server_sniffer_utils.mongo_helper as mh

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
DB_NAME = os.environ.get("DB_NAME")

INVENTORY_FILE_PATH = os.environ.get("INVENTORY_FILE_PATH")
NUM_WORKING_PROCS = os.environ.get("NUM_WORKING_PROCS")
ROTATION = os.environ.get("ROTATION")


def main():
    mongo_helper = mh.MongoHelper(DB_NAME, MONGO_HOST, MONGO_PORT)

    collection_names = mongo_helper.get_collection_names()
    collection_dates = [mongo_helper.get_collection_date(col_name) for col_name in collection_names if col_name != DB_NAME]
    oldest_collection_date = min(collection_dates) if collection_dates else None
    today_date = datetime.date.today()

    if collection_dates and (today_date - oldest_collection_date).days > ROTATION:
        mongo_helper.drop_collection(mongo_helper.get_collection_name(oldest_collection_date))

    today_collection_name = mongo_helper.get_collection_name(datetime.date.today())

    if (today_collection_name not in collection_names):
        mongo_helper.create_collection(today_collection_name)
        ansible_gatherer = ag.AnsibleGatherer(INVENTORY_FILE_PATH)
        print(INVENTORY_FILE_PATH, file='/usr/src/server_sniffer/out.log')

        with Pool(NUM_WORKING_PROCS) as p:
            docs = p.map(ansible_gatherer.gather_server_info, ansible_gatherer.get_server_names())

        mongo_helper.insert_documents(today_collection_name, docs)


if __name__ == "__main__":
    main()
