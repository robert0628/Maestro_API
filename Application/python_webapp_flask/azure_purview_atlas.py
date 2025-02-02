import os
from unittest import skip
from datetime import datetime
import requests
import json
from requests.auth import HTTPBasicAuth

from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient, AtlasEntity, AtlasProcess
from pyapacheatlas.core.util import AtlasException
from pyapacheatlas.core.glossary import PurviewGlossaryTerm



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

def atlas_api_search(query):
    client = atlas_client_connection()
    results = []
    if query is not None:
        search_by = query
        search = client.discovery.search_entities(search_by)
        if search is not None:
            for entity in search:
                results.append(entity)
    else:
        query = ""
        search = client.discovery.search_entities(search_by)
        if search is not None:
            for entity in search:
                results.append(entity)
    return results
    # search = client.discovery.search_entities("name:demo*")
    # search = client.discovery.search_entities("qualifiedName:demo*")

def atlas_api_read_classification():
    client = atlas_client_connection()
    try:
        single_class_check = client.get_entity_classification(
            guid="b58fc81e-a85f-4dfc-aad1-ee33b3421b87",
            classificationName="MICROSOFT.PERSONAL.IPADDRESS"
        )
        print(json.dumps(single_class_check, indent=2))
    except AtlasException as e:
        print("The provided classification was not found on the provied entity.")
        print(e)

    # You can also get ALL of the classifications from a given entity
    all_class_check = client.get_entity_classifications(
        guid="b58fc81e-a85f-4dfc-aad1-ee33b3421b83"
    )
    print(json.dumps(all_class_check, indent=2))
def atlas_api_glosary(glossary):
    client = atlas_client_connection()
    if glossary is not None:
        custom_glossary = client.glossary.get_glossary(glossary)
        return custom_glossary
    else:
        default_glossary = client.glossary.get_glossary()
        return default_glossary

def atlas_api_glosary_terms(query):
    client = atlas_client_connection()
    glossary_term = client.glossary.get_term(query)
    return glossary_term
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
    for list in enumDefs:
        for item in list:
            enumDefsGuids += item["guid"]
    print(enumDefsGuids)                   
    return

entity_obj = {}
entity_obj["name"] = "Cui Sqline Demo table"
entity_obj["typeName"] = "demoSqlite_table"
entity_obj["qualified_name"] = "somedb.schema.demoSqlitetable"
entity_obj["guid"] = -1000

obj = entity_obj

def atlas_api_create_entity(client, obj):
    # Create a new entity
    atlas_entity = AtlasEntity(obj)

    upload_results = client.upload_entities([atlas_entity])
    return upload_results