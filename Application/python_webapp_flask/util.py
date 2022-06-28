from .data_insight import *
from .process_nodes import *
from .rules import *
from .user_interface import *





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
