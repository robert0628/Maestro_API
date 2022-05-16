import inspect
import json
from datetime import datetime
from msilib.schema import Error

from azure.identity import ClientSecretCredential
from azure.core.exceptions import HttpResponseError

from azure.purview.catalog import PurviewCatalogClient
from azure.purview.scanning import PurviewScanningClient

from .azure_purview_operations import *

# Environment variables - need to be secured
tenantId = "ababe4b8-e9ca-48b1-910a-9a632c08bff2"
clientId = "d7b2cf84-1728-4ebc-a7ed-f2a4f1fa8dfe"
clientSecret = "a~Z8Q~i5zsaWLO5.HdPtxRSWNpyMaquqWadP7ajQ"
account = "democui"

# Config loader from json file
# config = json.load(open('aad_client.json'))
# for key, val in config.items():
#     if key == "tenantId":
#         tenantId = val
#     elif key == "clientId":
#         clientId = val
#     elif key == "secretId":
#         clientSecret = val
#     elif key == "account":
#         acc_name = val

def purview_client(model):
    credential = ClientSecretCredential(tenantId, clientId, clientSecret)
    purview_url = "https://{}.purview.azure.com".format(account)
    purview_scan_url = "https://{}.scan.purview.azure.com".format(account)
    if model == "catalog":
        client = PurviewCatalogClient(endpoint=purview_url, credential=credential)
    elif model == "scan":    
        client = PurviewScanningClient(endpoint=purview_scan_url, credential=credential)
    return client

def purview_data_scan(operation, data):
    client = purview_client("scan")
    operation_params = {}
    response = {}
    try:
        operation_params = data
        scan_cls = operation.split(":")[0]
        scan_op = operation.split(":")[1]
        scan_client = getattr(client, scan_cls)
        method = getattr(scan_client, scan_op)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if operation_params is not None and len(operation_params) == 0:
            result = method()
            resp_data = [item for item in result]
            return resp_data
        elif operation_params is not None and len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(**operation_params)
                    resp_data = [item for item in result]
                    return resp_data
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid."
            return response
    except Exception as err:
            response["Error"] = err
            return response

def purview_catalog_entity(operation, data):
    client = purview_client("catalog")
    entity = client.entity
    operation_params = {}
    response = {}
    try:
        operation_params = data
        method = getattr(entity, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if operation_params is not None and len(operation_params) == 0:
            result = method()
            return result
        elif operation_params is not None and len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(**operation_params)
                    return result
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid."
            return response
    except Exception as err:
            response["Error"] = err
            return response

def purview_catalog_glossary(operation, data):
    client = purview_client("catalog")
    glossary = client.glossary
    operation_params = {}
    response = {}
    try:
        operation_params = data
        method = getattr(glossary, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if operation_params is not None and len(operation_params) == 0:
            result = method()
            return result
        elif operation_params is not None and len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(**operation_params)
                    
                    return result
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid."
            return response
    except Exception as err:
            response["Error"] = err
            return response
def purview_catalog_discovery(operation, data):
    client = purview_client("catalog")
    discovery = client.discovery
    operation_params = {}
    response = {}
    try:
        operation_params = data
        method = getattr(discovery, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if operation_params is not None and len(operation_params) == 0:
            result = method()
            return result
        elif operation_params is not None and len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(**operation_params)
                    
                    return result
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid."
            return response
    except Exception as err:
            response["Error"] = err
            return response

def purview_catalog_lineage(operation, data):
    client = purview_client("catalog")
    lineage = client.lineage
    operation_params = {}
    response = {}
    try:
        operation_params = data
        method = getattr(lineage, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if operation_params is not None and len(operation_params) == 0:
            result = method()
            return result
        elif operation_params is not None and len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(**operation_params)
                    
                    return result
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid."
            return response
    except Exception as err:
            response["Error"] = err
            return response

def purview_catalog_relationship(operation, data):
    client = purview_client("catalog")
    relationship = client.relationship
    operation_params = {}
    response = {}
    try:
        operation_params = data
        method = getattr(relationship, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if operation_params is not None and len(operation_params) == 0:
            result = method()
            return result
        elif operation_params is not None and len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(**operation_params)
                    
                    return result
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid."
            return response
    except Exception as err:
            response["Error"] = err
            return response

def purview_catalog_types(operation, data):
    client = purview_client("catalog")
    types = client.types
    operation_params = {}
    response = {}
    try:
        operation_params = data
        method = getattr(types, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if operation_params is not None and len(operation_params) == 0:
            result = method()             
            return result
        elif operation_params is not None and len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(**operation_params)
                    
                    return result
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid, missing or required."
            return response
    except Exception as err:
            response["Error"] = err
            return response
def purview_catalog_collection(operation, data):
    client = purview_client("catalog")
    collection = client.collection
    operation_params = {}
    response = {}
    try:
        operation_params = data
        method = getattr(collection, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if operation_params is not None and len(operation_params) == 0:
            result = method()
            return result
        elif operation_params is not None and len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(**operation_params)
                    
                    return result
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid."
            return response
    except Exception as err:
            response["Error"] = err
            return response