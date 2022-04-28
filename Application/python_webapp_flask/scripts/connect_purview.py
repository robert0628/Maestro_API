import json
import threading
import time
from requests import request
from requests.auth import HTTPBasicAuth

cui_url = "http://localhost:5555/api/cui"

def get_purview():
    response = request("GET", cui_url, auth=HTTPBasicAuth('test', 'local'))
    