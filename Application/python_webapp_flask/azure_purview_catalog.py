## Info over GET, POST, DELETE Operations and data format requirements:
# operations need to follow the strict Purview Catalog Python SDK operation naming convention for each class type, bellow is the full list.
# Classes: glossary, entity, relationship, lineage, discovery, types and collection
# each class coreleates to respective endpoint functionality
# ex. Glossary class is available via /api/cui/purview/glossary with the operation as a required request param ex.: /api/cui/purview/types?operation=delete_type_by_name
# Full operation list available in DOC: https://azuresdkdocs.blob.core.windows.net/$web/python/azure-purview-catalog/1.0.0b3/azure.purview.catalog.operations.html
# Data objects that are passed with the requests to each operation, need to be wrapped with the respective operation function parameters by exact naming convention,
# in this sense we will take for example the discovery operation suggest (check Azure Docs: DiscoveryOperations) which takes as operation function param "suggest_request"
# for the data object in the request POST ../discovery?operation=suggest to be valid it will have to be wrapped as the prameter type, in this case the "suggest_request" is
# a JSONType object, the exact data object passed will be ex.:
# {
#     "suggest_request": {
#         "keywords": "DOD",
#         "limit": 0
#     } # JSONType Object
# }
# if the request is valid, the response will provide the respective Purview data as Content-Type: application/json, or the success of the operation as status code. 
# Request data needs to follow specific formatting and the correct key pair value input where required.
# -- potential changes - error handling response, return for Null data responses or csv IO response. 
# ex. {
#    "results": null
#}
# catch None responses and pass status_code in this case 200 OK or 204 No Content.
# All results from Purview catalog operations are returned as a JSON Object with the response values inside the "results" property.
# 
#  Official DOC: https://docs.microsoft.com/en-us/python/api/azure-purview-catalog/azure.purview.catalog.operations?view=azure-python-preview
#
import inspect
from datetime import datetime

from azure.purview.catalog import PurviewCatalogClient
from azure.identity import ClientSecretCredential
from azure.core.exceptions import HttpResponseError
from .azure_purview_operations import *


# Environment variables - need to be secured
tenantId = "ababe4b8-e9ca-48b1-910a-9a632c08bff2"
clientId = "d7b2cf84-1728-4ebc-a7ed-f2a4f1fa8dfe"
clientSecret = "a~Z8Q~i5zsaWLO5.HdPtxRSWNpyMaquqWadP7ajQ"
acc_name = "democui"

def purview_client():
    credential = ClientSecretCredential(tenantId, clientId, clientSecret)
    client = PurviewCatalogClient(endpoint="https://{}.purview.azure.com".format(acc_name), credential=credential)
    return client

def purview_catalog():
    client = purview_client()
    try:
        response = client.types.get_all_type_definitions()
        # print out all of your entity definitions
        return response
    except HttpResponseError as err:
        response = {}
        response["Error"] = err
        return response

# def purview_request_args(obj):    
#     args = {}
#     if obj is not None:
#         for key in obj:
#             if type(obj[key]) == 'list':
#                 args["list"] = obj[key]
#             elif type(obj[key]) == 'dict':
#                 args["object"] = obj[key]
#             elif type(obj[key]) == 'str':
#                     args["str"] = obj[key]
#         return args
#     else:
#         args = None
#         return args

def purview_catalog_entity(operation, data):
    client = purview_client()
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
    except HttpResponseError as err:
            response["Error"] = err
            return response

def purview_catalog_glossary(operation, data):
    client = purview_client()
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
                    print(result)
                    return result
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid."
            return response
    except HttpResponseError as err:
            response["Error"] = err
            return response
def purview_catalog_discovery(operation, data):
    client = purview_client()
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
                    print(result)
                    return result
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid."
            return response
    except HttpResponseError as err:
            response["Error"] = err
            return response

def purview_catalog_lineage(operation, data):
    client = purview_client()
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
                    print(result)
                    return result
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid."
            return response
    except HttpResponseError as err:
            response["Error"] = err
            return response

def purview_catalog_relationship(operation, data):
    client = purview_client()
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
                    print(result)
                    return result
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid."
            return response
    except HttpResponseError as err:
            response["Error"] = err
            return response

def purview_catalog_types(operation, data):
    client = purview_client()
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
                    print(result)
                    return result
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid."
            return response
    except HttpResponseError as err:
            response["Error"] = err
            return response
def purview_catalog_collection(operation, data):
    client = purview_client()
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
                    print(result)
                    return result
        else:
            response["Error"] = "Only JSON Data as Content-Type: application/json is valid."
            return response
    except HttpResponseError as err:
            response["Error"] = err
            return response
