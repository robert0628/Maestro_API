from operator import contains
from queue import Empty
from azure.purview.catalog import PurviewCatalogClient
from azure.identity import ClientSecretCredential
from azure.core.exceptions import HttpResponseError
from .azure_purview_operations import *
import inspect

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

def purview_request_args(obj):    
    args = {}
    if obj is not None:
        for key in obj:
            if type(obj[key]) == 'list':
                args["list"] = obj[key]
            elif type(obj[key]) == 'dict':
                args["object"] = obj[key]
            elif type(obj[key]) == 'str':
                if key == "guid":
                    args["guid"] = key
                elif key == "name":
                    args["name"] = key
        return args
    else:
        args = None
        return args

def purview_catalog_entity(operation, data):
    client = purview_client()
    entity = client.entity
    operation_params = {}
    response = {}

    if operation in entity_operations:
        pass
    else:
        response["Error"] = "Operation not Supported!"
        return response
    try:
        operation_params = data
        method = getattr(entity, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if len(operation_params) == 0:
            result = method()
            return result
        elif len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(*operation_params)
    except HttpResponseError as err:
            response["Error"] = err
            return response

def purview_catalog_glossary(operation, data):
    client = purview_client()
    glossary = client.glossary
    operation_params = {}
    response = {}
    
    if operation in glossary_operations:
        pass
    else:
        response["Error"] = "operation not Supported!"
        return response
    
    try:
        operation_params = data
        method = getattr(glossary, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if len(operation_params) == 0:
            result = method()
            return result
        elif len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(*operation_params)
    except HttpResponseError as err:
            response["Error"] = err
            return response
def purview_catalog_discovery(operation, data):
    client = purview_client()
    discovery = client.discovery
    operation_params = {}
    response = {}

    if operation in discovery_operations:
        pass
    else:
        response["Error"] = "operation not Supported!"
        return response
    try:
        operation_params = data
        method = getattr(discovery, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if len(operation_params) == 0:
            result = method()
            return result
        elif len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(*operation_params)
    except HttpResponseError as err:
            response["Error"] = err
            return response

def purview_catalog_lineage(operation, data):
    client = purview_client()
    lineage = client.lineage
    operation_params = {}
    response = {}


    if operation in lineage_operations:
        pass
    else:
        response["Error"] = "operation not Supported!"
        return response
    try:
        operation_params = data
        method = getattr(lineage, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if len(operation_params) == 0:
            result = method()
            return result
        elif len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(*operation_params)
    except HttpResponseError as err:
            response["Error"] = err
            return response

def purview_catalog_relationship(operation, data):
    client = purview_client()
    relationship = client.relationship
    operation_params = {}
    response = {}

    if operation in relationship_operations:
        pass
    else:
        response["Error"] = "operation not Supported!"
        return response

    try:
        operation_params = data
        method = getattr(relationship, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if len(operation_params) == 0:
            result = method()
            return result
        elif len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(*operation_params)
    except HttpResponseError as err:
            response["Error"] = err
            return response

def purview_catalog_types(operation, data):
    client = purview_client()
    types = client.types
    operation_params = {}
    response = {}

    if operation in types_operations:
        pass
    else:
        response["Error"] = "operation not Supported!"
        return response   
    try:
        operation_params = data
        method = getattr(types, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if len(operation_params) == 0:
            result = method()
            return result
        elif len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(*operation_params)
    except HttpResponseError as err:
            response["Error"] = err
            return response
def purview_catalog_collection(operation, data):
    client = purview_client()
    collection = client.collection
    operation_params = {}
    response = {}
    if operation in collection_operations:
        pass
    else:
        response["Error"] = "operation not Supported!"
        return response
    try:
        operation_params = data
        method = getattr(collection, operation)
        method_details = inspect.signature(method)
        method_params = list(method_details.parameters)
        if len(operation_params) == 0:
            result = method()
            return result
        elif len(operation_params) > 0:
            for param in method_params:
                if param in operation_params:
                    # print(operation_params[param])
                    result = method(*operation_params)
    except HttpResponseError as err:
            response["Error"] = err
            return response
