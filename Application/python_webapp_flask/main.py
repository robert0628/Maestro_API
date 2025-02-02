from importlib import resources
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS, cross_origin
from requests.auth import HTTPBasicAuth
import re
import json
import requests
import yaml
from werkzeug.exceptions import HTTPException

from python_webapp_flask.data_insight import augment_data
from python_webapp_flask import azure_cog_search

from .updating_links import *
from .rules import *
from .live_traffic import *
from .process_nodes import *
from .user_interface import *
from .data_insight import *
from .app_rationalization import *
from .RCAA_functions import *
from .azure_purview import *
from .update_nodes import *
from .azure_purview_atlas import *
from .azure_purview_api import *
from .util import *

from apscheduler.schedulers.background import BackgroundScheduler
from .scripts.connect_ssh import get_new_jsons

get_new_jsons()
scheduler = BackgroundScheduler()
scheduler.add_job(func=get_new_jsons, trigger="interval", minutes=10)
scheduler.start()

app = Flask(__name__)
cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_HEADERS'] = 'Content-Type'

from .graphQL import module as graphql_module
app.register_blueprint(graphql_module)

cliUrl = "https://71.25.48.225/api/cli"
envUrl = "https://71.25.48.225/api/monitoring/connections"

def call_api(payload = 0):
    with requests.Session() as session:
        session.verify = False

        headers = {
        'User-Agent': 'REST API Agent',
        'Content-Type': 'application/json'
        }
        if(payload == 0):
            response = session.request("GET", envUrl, auth=HTTPBasicAuth('pcglabs', 'TheMarsian'),  headers=headers)
        else:
            response = session.post(url=cliUrl,
                                auth=HTTPBasicAuth('pcglabs', 'TheMarsian'),
                                headers=headers,
                                data=json.dumps(payload),
                                )
    return response.json()


@app.route('/api/start_traffic_capture', methods=['GET'])
@cross_origin()
def start_traffic_capture():
    if request.method == 'GET':
        # To-Do to change for each client
        payload = {"commands": ["capture pc-traffic2 interface INSIDE match ip any any"]}

        response = call_api(payload)
        resp = jsonify("OK")
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp

@app.route('/api/auto_graph', methods=['GET'])
@cross_origin()
def auto_graph():
    if request.method == 'GET':
        json_file = json.load(open('generated.json'))
        response_data = [get_nodes(json_file, False, [])]
        response_data.append(get_ui_element(response_data))
        response_data[1]["ObjectType"] = generate_ui_techknow(response_data)

        process_auto_graph_data(response_data[0], json_file)

        response_data[0]["nodes"] = auto_graph_generate_nodes(response_data[0]["nodes"], json_file)
        
        return jsonify(response_data[0])
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp

@app.route('/api/live_graph', methods=['GET'])
@cross_origin()
def live_graph():
    if request.method == 'GET':
        json_file = json.load(open('generated.json'))
        response_data = [get_nodes(json_file, False, [])]
        response_data.append(get_ui_element(response_data))
        response_data[1]["ObjectType"] = generate_ui_techknow(response_data)

        outside_changes_color(response_data[0])
        process_live_data(response_data[0], json_file)

        response_data[0]["nodes"] = live_graph_generate_nodes(response_data[0]["nodes"], json_file)

        for el in response_data[0]["links"]:
            if el["value"] < 50:
                colour_gradient_list = colour_gradient("#00FF00", "#FFFF00", 50)
                el["color"] = colour_gradient_list[el["value"]].hex
            else:
                colour_gradient_list = colour_gradient("#FFFF00", "#FF0000", 50)
                el["color"] = colour_gradient_list[el["value"] - 1 - 50].hex

        return jsonify(response_data[0])
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp


@app.route('/api/search', methods=['POST'])
@cross_origin()
def cognitve_search():
    if request.method == 'POST':
        
        response = {}

        params = request.json
        search_text = params["searchText"]
        # index_name = params["indexName"]
        page_size = params['pageSize'] if 'pageSize' in params and params['pageSize'] else 10
        page_no = params['pageNo'] if 'pageNo' in params and params['pageNo'] else 1


        azure_indexes = ["auto-graph-links-index", "auto-graph-nodes-index", "live-graph-links-index", "live-graph-nodes-index", "mono-2-micro-app-index", "mono-2-micro-clusters-index", "mono-2-micro-datasets-index", "mono-2-micro-hosts-index", "mono-2-micro-links-index", "mono-2-micro-nodes-index", "mono-2-micro-services-index", "mono2-micro-table-index", "azureblob-index"]
        for azure_index in azure_indexes:
            temp_dict = {}
            result = azure_cog_search.search(search_text=search_text, index_name=azure_index, page_size=page_size, page_no=page_no)        
            
            documents = []
            for item in result:
                documents.append(item)
            
            temp_dict["count"] = result.get_count()
            temp_dict["data"] = documents
            response[azure_index] = temp_dict
        return jsonify(response)
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp



@app.route('/api/mono_2_micro', methods=['GET'])
@cross_origin()
def mono_2_micro():
    if request.method == 'GET':
        response_data = generate_mono_2_micro()
        nodes, links = response_data[0]["nodes"], response_data[0]["links"]
        applications, services, hosts, databases, groups = augment_data(nodes, links)

        response_data[0]["app"] = applications
        response_data[0]["services"] = services
        response_data[0]["hosts"] = hosts
        response_data[0]["datasets"] = databases
        response_data[0]["clusters"] = groups
        add_links_applications_hosts(response_data)
        add_links_hosts_services(response_data)
        add_links_hosts_datasets(response_data)
        add_apps_nodes(response_data)
        add_hosts_nodes(response_data)
        for elem in response_data[0]['clusters']:
            for node in elem['nodes']:
                try:
                    name = node['name']
                except:
                  node['name'] = ''
        for node in response_data[0]['nodes']:
            try:
                name = node['name']
            except:
                node['name'] = ''
        
        return jsonify(response_data[0])
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp

from vm_recommendations import vm_recommendation
@app.route('/api/hardware_2_cloud', methods=['GET'])
@cross_origin()
def hardware_2_cloud():
    if request.method == 'GET':
        initial_data = json.load(open('generated.json'))
        response_data = generate_mono_2_micro()
        applications, services, hosts, databases, groups = augment_data(response_data[0]["nodes"],response_data[0]["links"])
        response_data[0]["clusters"] = groups
        response = jsonify(vm_recommendation(response_data, initial_data))
        return(response)

    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp

@app.route('/api/get_containerization_model', methods=['GET'])
@cross_origin()
def get_containerization_model():
    if request.method == 'GET':
        data = generate_mono_2_micro()
        clusters = get_clusters(data[0]["nodes"])      
        return jsonify(get_contain(clusters))
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp


@app.route('/api/rcaa', methods=["GET"])
@cross_origin()
def rcaa():
    if request.method == 'GET':
        response_data = return_structure()
        return jsonify(response_data)
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp



@app.route('/api/app_rationalization', methods=['GET'])
@cross_origin()
def app_rationalization():
    if request.method == 'GET':
        page_size = request.args.get('pageSize', 1000)
        response = create_app_rationalization_stucture(page_size)
        return jsonify(response)
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp

# Independent API Endpoint that uses Azure Custom Authorization and custom Purview REST API's, Azure Oauth2.0 Provider: https://login.microsoftonline.com//api/{Tenant}/oauth2/v2.0/token
# $source azure_purview.py 
@app.route('/api/cui', methods=['GET'])
@cross_origin()
def cui():
    if request.method == 'GET':
        data = create_cui_stucture()
        resp = jsonify(data)
        return resp
        #return jsonify(response)
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp

# Independent API Endpoint impemented with Python SDK for Azure Purview and Apache Atlas (pyapacheatlas) Official DOC: https://github.com/wjohnson/pyapacheatlas
# $source azure_purview_atlas.py 
@app.route('/api/cui/atlas', methods=['GET'])
@cross_origin()
def atlas():
    if request.method == 'GET':
        data = atlas_api_get_type_def()
        #resp = jsonify(success=True)
        resp = jsonify(data)
        return resp
        #return jsonify(response)
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp

@app.route('/api/cui/atlas/glossary', methods=['GET', 'POST', 'DELETE'])
@cross_origin()
def atlas_glossary():
    if request.method == 'GET':
        glossary = "Glossary"
        data = atlas_api_glosary(glossary)
        #resp = jsonify(success=True)
        resp = jsonify(data)
        return resp
        #return jsonify(response)
    elif request.method == 'POST':

        response = {}

        params = request.json
        
        input_field1 = params["searchText"]
        input_field2 = params["searchType"]

        data = atlas_api_glosary(input_field1)
        #resp = jsonify(success=True)
        resp = jsonify(data)
        return resp
        #return jsonify(response)
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp

@app.route('/api/cui/atlas/glossary/terms', methods=['GET', 'POST', 'DELETE'])
@cross_origin()
def atlas_glossary_terms():
    if request.method == 'GET':
        glossary = "Glossary"
        data = atlas_api_glosary(glossary)
        #resp = jsonify(success=True)
        resp = jsonify(data)
        return resp
        #return jsonify(response)
    elif request.method == 'POST':

        response = {}
        params = request.json       
        input_field1 = params["guid"]
        data = atlas_api_glosary_terms(input_field1)
        #resp = jsonify(success=True)
        resp = jsonify(data)
        return resp
        #return jsonify(response)
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp        

@app.route('/api/cui/atlas/search', methods=['POST'])
@cross_origin()
def atlas_search():
    if request.method == 'POST':
        
        response = {}

        params = request.json
        search_text = params["searchText"]
        search_type = params["searchType"]

        result = atlas_api_search(search_text)
    
        # for item in result:
        #     atlas_search.append(item)
        
        response["count"] = result.get_count()
        response["results"] = result

        return jsonify(response)
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp

# Azure Purview Catalog Python SDK 1.0.3b Official DOC: https://docs.microsoft.com/en-us/dotnet/api/overview/azure/analytics.purview.catalog-readme-pre
# $source azure_purview_catalog.py

@app.route('/api/cui/purview/entity', methods=['GET','POST','DELETE'])
@cross_origin()
def purview_api_entity():
    args = request.args
    response = {}
    data = {}
    if "operation" in args:
        operation = args.get("operation")
    else:
        operation = ""
    if operation in entity_operations:
        pass
    else:
        response["Error"] = "Operation not Supported!"
        response = jsonify(response)
        response.status_code = 405
        return response
    if request.method == 'GET':
        result = purview_catalog_entity(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    elif request.method == 'POST':
        data = request.json
        result = purview_catalog_entity(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    elif request.method == 'DELETE':
        data = request.json
        result = purview_catalog_entity(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    else:
        response = jsonify(success=False)
        response.status_code = 405
        return response

@app.route('/api/cui/purview/glossary', methods=['GET','POST','DELETE'])
@cross_origin()
def purview_api_glossary():
    args = request.args
    response = {}
    data = {}
    if "operation" in args:
        operation = args.get("operation")
    else:
        operation = ""
    if operation in glossary_operations:
        pass
    else:
        response["Error"] = "Operation not Supported!"
        response = jsonify(response)
        response.status_code = 405
        return response
    if request.method == 'GET':
        result = purview_catalog_glossary(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    elif request.method == 'POST':
        data = request.json
        result = purview_catalog_glossary(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    elif request.method == 'DELETE':
        data = request.json
        result = purview_catalog_glossary(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    else:
        response = jsonify(success=False)
        response.status_code = 405
        return response

@app.route('/api/cui/purview/discovery', methods=['GET','POST'])
@cross_origin()
def purview_api_discovery():
    args = request.args
    response = {}
    data = {}
    if "operation" in args:
        operation = args.get("operation")
    else:
        operation = ""
    if operation in discovery_operations:
        pass
    else:
        response["Error"] = "Operation not Supported!"
        response = jsonify(response)
        response.status_code = 405
        return response
    if request.method == 'POST':
        data = request.json
        result = purview_catalog_discovery(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    else:
        response = jsonify(success=False)
        response.status_code = 405
        return response

@app.route('/api/cui/purview/lineage', methods=['GET'])
@cross_origin()
def purview_api_lineage():
    args = request.args
    response = {}
    data = {}
    if "operation" in args:
        operation = args.get("operation")
    else:
        operation = ""
    if operation in lineage_operations:
        pass
    else:
        response["Error"] = "Operation not Supported!"
        response = jsonify(response)
        response.status_code = 405
        return response
    if request.method == 'GET':
        result = purview_catalog_lineage(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    else:
        response = jsonify(success=False)
        response.status_code = 405
        return response

@app.route('/api/cui/purview/relationship', methods=['GET','POST','DELETE'])
@cross_origin()
def purview_api_relationship():
    args = request.args
    response = {}
    data = {}
    if "operation" in args:
        operation = args.get("operation")
    else:
        operation = ""
    if operation in relationship_operations:
        pass
    else:
        response["Error"] = "Operation not Supported!"
        response = jsonify(response)
        response.status_code = 405
        return response
    if request.method == 'GET':
        result = purview_catalog_relationship(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    elif request.method == 'POST':
        data = request.json
        result = purview_catalog_relationship(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    elif request.method == 'DELETE':
        data = request.json
        result = purview_catalog_relationship(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    else:
        response = jsonify(success=False)
        response.status_code = 405
        return response

@app.route('/api/cui/purview/types', methods=['GET','POST','DELETE'])
@cross_origin()
def purview_api_types():
    args = request.args
    response = {}
    data = {}
    if "operation" in args:
        operation = args.get("operation")
    else:
        operation = ""
    if operation in types_operations:
        pass
    else:
        response["Error"] = "Operation not Supported!"
        response = jsonify(response)
        response.status_code = 405
        return response
    if request.method == 'GET':
        result = purview_catalog_types(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    elif request.method == 'POST':
        data = request.json
        result = purview_catalog_types(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    elif request.method == 'DELETE':
        data = request.json
        result = purview_catalog_types(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    else:
        response = jsonify(success=False)
        response.status_code = 405
        return response

@app.route('/api/cui/purview/collection', methods=['POST'])
@cross_origin()
def purview_api_collection():
    args = request.args
    response = {}
    data = {}
    if "operation" in args:
        operation = args.get("operation")
    else:
        operation = ""
    if operation in collection_operations:
        pass
    else:
        response["Error"] = "Operation not Supported!"
        response = jsonify(response)
        response.status_code = 405
        return response
    if request.method == 'POST':
        data = request.json
        result = purview_catalog_collection(operation, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)         
    else:
        response = jsonify(success=False)
        response.status_code = 405
        return response

# Azure Purview Scanning Python SDK 1.0.0b2 Official DOC: https://azuresdkdocs.blob.core.windows.net/$web/python/azure-purview-scanning/1.0.0b2/index.html
@app.route('/api/cui/purview/scan/<cls>', methods=['GET','POST','DELETE'])
@cross_origin()
def purview_api_data_scan(cls):
    allowed_cls = [ cls for cls, ops in scan_client_operations.items()]
    args = request.args
    response = {}
    data = {}
    if "operation" in args:
        operation = args.get("operation")
    else:
        operation = ""

    if cls in allowed_cls:
        pass
    else:
        response["Error"] = "Endpoint not Supported!"
        response = jsonify(response)
        response.status_code = 405
        return response
    for c,ops in scan_client_operations.items():
        if cls == c:
            if operation in ops:
                model_op = c + ":" + operation
                pass
            else:
                response["Error"] = "Operation not Supported!"
                response = jsonify(response)
                response.status_code = 405
                return response

    if request.method == 'GET':
        result = purview_data_scan(model_op, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    elif request.method == 'POST':
        data = request.json
        result = purview_data_scan(model_op, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    elif request.method == 'DELETE':
        data = request.json
        result = purview_data_scan(model_op, data)
        if result is not None:
            if "Error" in result:
                print(result) # do something with error message
                response = jsonify("Operation Failure!")
                response.status_code = 400
                return response
            else:
                response["results"] = result
        return jsonify(response)
    else:
        response = jsonify(success=False)
        response.status_code = 405
        return response