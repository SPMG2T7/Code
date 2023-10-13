import meilisearch
import requests
import time
from os import getenv
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from datetime import datetime

load_dotenv()
SEARCH_MASTER_KEY = getenv('SEARCH_MASTER_KEY')

# Start-Connecting to MeiliSearch
client = meilisearch.Client('http://host.docker.internal:7700', SEARCH_MASTER_KEY)
r = requests.get('http://host.docker.internal:5000/roles/get_all')


if r.status_code != requests.codes.ok:
    code = r.status_code
try:
    print('inside try')
    result = r.json() if len(r.content)>0 else ""

    roles = result['data']['roles']
    for role in roles:
        print(role)
        client.index('roles').add_documents([
                {
                    "role_id": role['role_id'],
                    "role_name": role['role_name'],
                    "role_description": role['role_description'],
                    "listed_by": role['listed_by'],
                    "no_of_pax": role['no_of_pax'],
                    "department": role['department'],
                    "expiry_date": role['expiry_date'],
                    "skills_required": role['skills_required'],
                    "location": role['location'],
                    "days_left": role['days_left'],
                    "count_applicant": 0
                }
            ], primary_key='role_id')
except Exception as e:
    code = 500
    print(str(e))