from importlib import resources
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from requests.auth import HTTPBasicAuth
import json
import requests
import yaml

from python_webapp_flask.data_insight import augment_data
from python_webapp_flask import azure_cog_search

from .updating_links import *
from .rules import *
from .live_traffic import *
from .process_nodes import *
from .user_interface import *
from .data_insight import *
from .roa import *
from .app_rationalization import *
from .RCAA_functions import *
from .roa import *
from .update_nodes import *

from apscheduler.schedulers.background import BackgroundScheduler
from .scripts.connect_ssh import get_new_jsons

get_new_jsons()
scheduler = BackgroundScheduler()
scheduler.add_job(func=get_new_jsons, trigger="interval", minutes=10)
scheduler.start()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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

def generate_data(boolean = True):
    response = json.load(open('generated.json'))
    response_data = [get_nodes(response, boolean, [])]
    response_data = apply_separation_rule(response_data)
    response_data = apply_rule2(response_data, select_microservice(response, 2))

    mapped_names = {}
    for item in response['items']:
        source = item['sourceIp'] + ":" + item['sourcePort']
        destination = item['destinationIp'] + ":" + item['destinationPort']
        mapped_names[source] = item['hostName']
        mapped_names[destination] = ''
    for node in response_data[0]['nodes']:
        node['name'] = mapped_names[node['id']]

    if(boolean):
        response_data[0], node_connections, max_edges = plot_nodes(response_data[0])
        response_data[0] = index_list(response_data[0])

        response_data[0] = set_specific_icons(response_data[0])
        json_connections = create_navbar_data(node_connections, max_edges, response_data[0])
        return response_data, json_connections
    else:
        return response_data

def generate_mono_2_micro():
    prev_data, json_connections = generate_data()

    prev_data = prev_data[0]
    response_data = []
    nodes, links = reformat_mono2micro(prev_data)
    list_to_add = {"nodes" : nodes, "links" : links}
    response_data.append(list_to_add)
    response_data.append(get_ui_element(prev_data, json_connections))
    contain = get_contain(get_clusters(response_data[0]["nodes"]))

    index = 0
    for elem in prev_data["nodes"]:
        if elem["cluster"] == 1:
            continue
        for elem3 in contain:
                for fields in elem3["containerAppService"]:
                    if str(elem["id"]).split(':')[0] in str(fields["name"]):
                        response_data[0]["nodes"][index]["containerID"] = fields["containerID"]
        index += 1
    outside_changes_color(response_data[0])
 
    return response_data

def get_contain(clusters):
    k8s_confs = []
    containers_unique_id, counter = {}, [0]
    for cluster, containers in clusters.items():
        k8s_conf = apply_k8s_config(cluster, containers, containers_unique_id, counter)
        k8s_confs.append(k8s_conf)
    return k8s_confs


def apply_k8s_config(cluster, containers, containers_unique_id, counter):
    images = []
    for container in containers:
        cpu_limits, memory_limits, cpu_requests, memory_requests = get_k8s_resources(container["requests"]) 
        ip, port = container["ip"], container["port"]
        if ip not in containers_unique_id:
            counter[0] += 1
            containers_unique_id["ip"] = counter[0]
        images.append({ 
            "image": f"server-{ip}-container-image",
            "name": f"Server-{ip}",
            "containerPort": port,
            "resources": {
                "limits": {
                    "cpu": cpu_limits,
                    "memory": memory_limits
                },
                "requests": {
                    "cpu": cpu_requests,
                    "memory": memory_requests
                }
            },
            "containerID": containers_unique_id["ip"]
        })
    k8s_conf_tmp = {
        "host":"Linux",
        "engine":"Docker",
        "appID": cluster,
        "clusterID": cluster,
        "cluster-2-appname": f"Cluster-{cluster}", 
        "containerAppService": images
    }
    
    return k8s_conf_tmp

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
        index_name = params["indexName"]

        result = azure_cog_search.search(search_text=search_text, index_name=index_name)        
        
        documents = []
        for item in result:
            documents.append(item)
        
        response["count"] = result.get_count()
        response["data"] = documents

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

@app.route('/api/get_mono_2_micro_table', methods=['GET'])
@cross_origin()
def get_mono_2_micro_table():
    if request.method == 'GET':
        response_data = generate_mono_2_micro()
        response = []
        for file in response_data[0]['nodes']:
            response.append({'Application' : file['id'], 'Complexity score' : 0, 'Size': 0, 'Host' : file['id'].split(':')[0], 'Number of services': 0, 'Number of processes': 0, 'Datacenters': 0, 'Number of dependencies' : 0})
        return jsonify(response)
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

@app.route('/api/rao', methods=['GET'])
@cross_origin()
def rao():
    if request.method == 'GET':
        json_file = json.load(open('generated.json'))
        node_data = [get_nodes(json_file, False, [])]
        response = create_roa_stucture(json_file, node_data)
        return jsonify(response)
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp

@app.route('/api/app_rationalization', methods=['GET'])
@cross_origin()
def app_rationalization():
    if request.method == 'GET':
        response = create_app_rationalization_stucture()
        return jsonify(response)
    else:
        resp = jsonify(success=False)
        resp.status_code = 405
        return resp
