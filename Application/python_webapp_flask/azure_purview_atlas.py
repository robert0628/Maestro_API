import os
from unittest import skip
from datetime import datetime
import requests
import json
from requests.auth import HTTPBasicAuth

from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
from pyapacheatlas.core import AtlasEntity

tenantId = "ababe4b8-e9ca-48b1-910a-9a632c08bff2"
clientId = "d7b2cf84-1728-4ebc-a7ed-f2a4f1fa8dfe"
clientSecret = "a~Z8Q~i5zsaWLO5.HdPtxRSWNpyMaquqWadP7ajQ"
cui_acc_name = "democui"

guids = []
guid = ""

def atlas_client_connection():
    auth = ServicePrincipalAuthentication(
        tenant_id = tenantId, 
        client_id = clientId, 
        client_secret = clientSecret
        )

    client = PurviewClient(
        account_name = cui_acc_name,
        authentication = auth
    )
    return client

def atlas_api_get_type_def():
    client = atlas_client_connection()
    # Get All Type Defs
    all_type_defs = client.get_all_typedefs()
    return all_type_defs

def atlas_api_get_entity_guids():
    all_type_defs = atlas_api_get_type_def()

    classificationDefs = []
    classificationDefsGuids = []

    entityDefs = []
    entityDefsGuids = []

    relationshipDefs = []
    relationshipDefsGuids = []
    
    structDefs = []
    structDefsGuids = []

    enumDefs = []
    enumDefsGuids = []
    
    for alist in all_type_defs:
        if alist == "enumDefs":
           enumDefs.append(all_type_defs[alist])
        elif alist == "classificationDefs":
            classificationDefs.append(all_type_defs[alist])
        elif alist == "relationshipDefs":
            relationshipDefs.append(all_type_defs[alist])
        elif alist == "entityDefs":
            entityDefs.append(all_type_defs[alist])
        elif alist == "structDefs":
            structDefs.append(all_type_defs[alist])                   
    return

def atlas_api_get_def_guids():
    client = atlas_client_connection()
    # Get Specific Entities
    list_of_entities = client.get_entity(guid=guids)
    return

obj = {}
obj["name"] = "Cui Sqline Demo table"
obj["typeName"] = "demoSqlite_table"
obj["qualified_name"] = "somedb.schema.demoSqlitetable"
obj["guid"] = -1000


def atlas_api_create_entity(client, obj):
    # Create a new entity
    atlas_entity = AtlasEntity(obj)

    upload_results = client.upload_entities([atlas_entity])
    return upload_results