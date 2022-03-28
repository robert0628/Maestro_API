from requests.auth import HTTPBasicAuth
import requests
from netaddr import IPNetwork
import json

netObjUrl = "https://71.25.48.225/api/objects/networkobjects"

def spawn_node(ip):
    return {
        "id":ip,
        "connections":0,
        "incoming":0,
        "outgoing":0,
        "svg":""
    }

def get_nodes(json_file, want_port, internal_nodes=[]):
    json_data = {
            "nodes":[],
            "links":[]
    }

    for obj in json_file['items']:
        ip0 = obj['sourceIp']      # sender
        port0 = obj['sourcePort']

        ip1 = obj['destinationIp']     # receiver
        port1 = obj['destinationPort']

        if ip0 in internal_nodes and ip1 in internal_nodes or len(internal_nodes) == 0:
            if(want_port):
                ip1 = ip1 +":"+ str(port1)

            if(want_port):
                ip0 = ip0 +":"+ str(port0)

            if not {"id":ip1, "connections":0, "incoming":0, "outgoing":0, "svg":""} in json_data['nodes']:
                json_data['nodes'].append(spawn_node(ip1))
            if not {"id":ip0, "connections":0, "incoming":0, "outgoing":0, "svg":""} in json_data['nodes']:
                json_data['nodes'].append(spawn_node(ip0))

            if not {"source":ip0,"target":ip1} in json_data['links']:
                json_data['links'].append({"source":ip0,"target":ip1})

    return json_data


def plot_nodes(response_data):
    data_connections = []

    max_connections = 0
    for node in response_data["nodes"]:
        if(node["connections"] > max_connections):
            max_connections = node["connections"]
    max_connections += 1

    for i in range(1, max_connections):
        temp_data = []
        for nodes in response_data["nodes"]:
            if(nodes["connections"] == i):
                new_data = []
                new_data.append(nodes["id"])
                temp_data.append(new_data)
        data_connections.append(temp_data)

    links = response_data["links"].copy()

    for i in range(0, len(data_connections)):
        for nodes in data_connections[i]:
            new_data = []
            for ids in nodes:
                new_data = recursive_links_search(ids, new_data, links)
            nodes.append(new_data)

    max = 0
    for connections_amount in data_connections:
        for connection in connections_amount:
            if(len(connection[1])):
                if(len(connection[1]) > max):
                    max = len(connection[1])

    i = 0
    j = 0

    data = modify_connections(data_connections, max)

    for z in range(1, max + 1):
        if(len(data[z])):
            for connection in data[z]:
                for node in response_data["nodes"]:
                    if(node["id"] == connection[0]):
                        node["cluster"] = z
                for elem in connection[1]:
                    for node in response_data["nodes"]:
                        if(node["id"] == elem):
                            node["cluster"] = z


    connections = []
    for connections_amount in data_connections:
        for connection in connections_amount:
            if(len(connection[1])):
                connections.append(connection)


    return(response_data, connections, max_connections)

def recursive_links_search(id_head, current_list, links, saw_nodes = []):
    new_links = links.copy()
    new_list = []
    for connection in new_links:
        if(connection["target"] == id_head and connection["target"] not in saw_nodes):
            saw_nodes.append(connection["target"])
            source = connection["source"]
        elif(connection["source"] == id_head and connection["target"] not in saw_nodes):
            saw_nodes.append(connection["source"])
            source = connection["target"]
        else:
            continue
        current_list.append(source)
        new_links.remove(connection)
        new_list = (recursive_links_search(source, current_list, new_links, saw_nodes))

    for connection in new_links:
        if(connection["target"] == id_head):
            new_list.append(connection["source"])

    current_list.extend(new_list)
    current_list = list(set(current_list))
    return current_list

def index_list(response_data):
    i = 0
    for node in response_data["nodes"]:
        node["index"] = i
        i += 1
    return response_data

def generate_inside_ips_list():
    with requests.Session() as session:
        session.verify = False
        headers = {
            'User-Agent': 'REST API Agent'
        }

        #Get all network objects of type IPv4Adress and add to list
        excludeResponse = session.request("GET", netObjUrl, auth=HTTPBasicAuth('pcglabs', 'TheMarsian'),  headers=headers)
        excludeResponse = excludeResponse.json()

        addresses = []
        for item in excludeResponse['items']:
            if 'host' in item.keys():
                if item['host']['kind'] == 'IPv4Network':
                    ip_addr , mask = item['host']['value'].split('/')

                    network = IPNetwork('/'.join([ip_addr, mask]))
                    generator = network.iter_hosts()
                    for elem in generator:
                        addresses.append(str(elem))
    return addresses

def outside_changes_color(response_data):
    addresses = generate_inside_ips_list()

    for link in response_data["links"]:
        source_ip = link["source"]
        target_ip = link["target"]
        try:
            source_ip = link["source"].split(":")[0]
            target_ip = link["target"].split(":")[0]
        except:
            pass

        if source_ip not in addresses:
            link["color"] = "#0000FF"
        else:
        # if target_ip in addresses:
            link["color"] = "#0000FF"

    return response_data


def modify_connections(data_connections, max):
    data = [None] * (max + 1)
    for i in range(1, max + 1):
        temp_data = []
        for connections_amount in data_connections:
            for connection in connections_amount:
                if(len(connection[1]) == i):
                    temp_data.append(connection)
        if(data[i] == None):
            data[i] = temp_data
        else:
            data[i].extend(temp_data)
    return data

def reformat_mono2micro(prev_data):
    nodes, groupId = [], []
    for elem in prev_data["nodes"]:
        if elem["cluster"] == 1:
            continue
        try:
            new_dict = {
                "id": elem["id"],
                "groupID": elem["cluster"] - 1,  
                "port" : str(elem["id"]).split(':')[1],
            }
            if not elem["cluster"] - 1 in groupId:
                groupId.append(elem["cluster"] - 1)
                new_dict["clusterID"] = len(groupId)
            else:
                new_dict["clusterID"] = groupId.index(elem["cluster"] - 1) + 1
            
            nodes.append(new_dict) 
        except:
            # this element is a fake node we created for clustering, so we do not need it
            pass
    links = []
    node_ids = [node["id"] for node in nodes]
    for elem in prev_data["links"]:
        if elem["target"] in node_ids and elem["source"] in node_ids:
            try:
                if(elem["opacity"] == 0):
                    pass
                # if the element has opacity, we do not need it, since that link is only used for clustering
            except:
                new_dict = {
                    "source": elem["source"],
                    "target": elem["target"],
                    "value": 0,
                    "typeConnect" : "ASYNC"
                }
                links.append(new_dict)
    return nodes, links