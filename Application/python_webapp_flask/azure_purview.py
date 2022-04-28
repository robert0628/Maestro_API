import os
from unittest import skip
from datetime import datetime
import requests
import json
from requests.auth import HTTPBasicAuth

from azure.identity import ClientSecretCredential

tenantId = "ababe4b8-e9ca-48b1-910a-9a632c08bff2"
clientId = "d7b2cf84-1728-4ebc-a7ed-f2a4f1fa8dfe"
clientSecret = "a~Z8Q~i5zsaWLO5.HdPtxRSWNpyMaquqWadP7ajQ"

aad_client_credentials = ClientSecretCredential(tenantId, clientId, clientSecret)
token_url = 'https://login.microsoftonline.com//api/{}/oauth2/v2.0/token'.format(tenantId)

guid = ""
scans = ""

accountUrl = 'https://democui.purview.azure.com/account?api-version=2019-11-01-preview'
collectionsUrl = "https://democui.purview.azure.com/collections?api-version=2019-11-01-preview"
datasourcesUrl = "https://democui.scan.purview.azure.com/datasources?api-version=2018-12-01-preview"
atlasEntityDefUrl = "https://democui.catalog.purview.azure.com/api/atlas/v2/types/typedefs"
atlasEntityTypesHeadersUrl = "https://democui.catalog.purview.azure.com/api/atlas/v2/types/typedefs/headers"
glosaryUrl = "https://democui.purview.azure.com/catalog/api/atlas/v2/glossary"

datasourcescansUrl = "https://democui.scan.purview.azure.com/datasources/{}/scans?api-version=2018-12-01-preview"
atlasEntityAuditUrl = 'https://democui.purview.azure.com/catalog/api/atlas/v2/entity/{}/audit'.format(guid)

datascansUrl = "https://democui.scan.purview.azure.com/datasources/{}/scans/?api-version=2018-12-01-preview"
scanUrl = "https://democui.scan.purview.azure.com/datasources/{}/scans/{}?api-version=2018-12-01-preview"

scope = "https://purview.azure.net/.default"


def aad_generate_token():
    response = aad_client_credentials.get_token(scope)
    if response.token is not None:
        access_token = response.token
    else:
        access_token = ""
    
    return access_token

def call_Purview_api_datasources_dict():
    accesstoken = aad_generate_token()

    headers = {
         'Accept' : 'application/json',
         'Authorization': 'Bearer '+accesstoken
    }
    
    datasources = requests.get(datasourcesUrl, verify = False, headers = headers)
    
    if datasources is not None:
        datasources_jsonResp = datasources.json()
        datasource_count = datasources_jsonResp["count"]
        datasources_value = datasources_jsonResp["value"]
    datasources_dict = datasources_value    

    return datasources_dict

def call_Purview_api_collections_dict():
    accesstoken = aad_generate_token()

    headers = {
         'Accept' : 'application/json',
         'Authorization': 'Bearer '+accesstoken
    }
    
    collections = requests.get(collectionsUrl, verify = False, headers = headers)
    
    if collections is not None:
        collections_jsonResp = collections.json()
        collections_value = collections_jsonResp["value"]
    collections_dict = collections_value    

    return collections_dict    

def call_Purview_api_datasource_scans():
    scans_dict = []

    accesstoken = aad_generate_token()
    headers = {
         'Accept' : 'application/json',
         'Authorization': 'Bearer '+accesstoken
    }
    
    datasources = call_Purview_api_datasources_dict()

    if datasources is not None:
        for datasource in datasources:
            scan_source = datasource["name"]
            datasource_scans_resp = requests.get(datascansUrl.format(scan_source), verify = False, headers = headers)
            json_datasource_scans = datasource_scans_resp.json()
            if(json_datasource_scans["value"] is not None):
                scans_data = json_datasource_scans["value"]
                for scan in scans_data:
                    scan_name = scan["name"]
                    scan_details = requests.get(scanUrl.format(scan_source, scan_name), verify = False, headers = headers)
                    scan_data = json.loads(scan_details.text)
                    scans_dict.append(scan_data)
    else:
        scans_dict = []
    return scans_dict


def call_Purview_api_atlas():
    
    accesstoken = aad_generate_token()

    headers = {
         'Accept' : 'application/json',
         'Authorization': 'Bearer '+accesstoken
    }
    
    atlas_resp = requests.get(atlasEntityDefUrl, verify = False, headers = headers)
    atlas_dict = atlas_resp.json()

    return atlas_dict

def add_datasources_data_cui(data):
    return

def add_collections_data_cui(data):
    return

def add_atlas_data_cui(data):
    return

def create_cui_stucture():
    cui_structure = {}
    cui_structure["datasources"] = call_Purview_api_datasources_dict()
    cui_structure["collections"] = call_Purview_api_collections_dict()
    cui_structure["scans"] = call_Purview_api_datasource_scans()
    cui_structure["atlas"] = call_Purview_api_atlas()
    #cui_structure["raGroup"] = add_datasources_data_cui(cui_structure["links"])
    #cui_structure["atlas"] = create_routeOpt_structure(json_file)

    return cui_structure