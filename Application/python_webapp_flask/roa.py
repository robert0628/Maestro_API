import random

def add_links_data_roa(json_file):
    links = []
    for item in json_file['items']:
        links.append({ 
            "source": item['sourceIp'],
            "target": item['destinationIp'],
            "datatype": item['protocol'],
            "rtTransitTime": random.choice(['1 ms', '2 ms', '3 ms', '5 ms'])
            })

    return links

def add_nodes_data_roa(json_file):
    nodes = []
    ipList = []

    for item in json_file['items']:
        if item['sourceIp'] not in ipList:
            ipList.append(item['sourceIp'])
            nodes.append({ 
            "Id": item['sourceIp'],
            "name": item['hostName'],
            "ip": item['sourceIp'],
            "dataType": item['protocol']
            })

        if item['destinationIp'] not in ipList:
            ipList.append(item['destinationIp'])
            nodes.append({ 
            "Id": item['destinationIp'],
            "name": item['hostName'],
            "ip": item['destinationIp'],
            "dataType": item['protocol']
            })

    return nodes

def add_ragroup_data_roa(links):
    ragroup = []
    routeId = 0
    for link in links:
        ragroup.append({ 
            "routeID": routeId,
            "routeName": "From " + str(link['source']) + " to " + str(link['target']),
            "tracer": "traceroute",
            "numberHops": 1
            })
        routeId += 1

    return ragroup

def add_routeOpt_links_data(json_file):
    links = []
    for item in json_file['items']:
        links.append({ 
            "source": item['sourceIp'],
            "target": item['destinationIp'],
            "datatype": item['protocol'],
            "rtTransitTime": random.choice(['1 ms', '2 ms', '3 ms', '5 ms'])
            })

    return links

def add_routeOpt_nodes_data(json_file):
    nodes = []
    ipList = []

    for item in json_file['items']:
        if item['sourceIp'] not in ipList:
            ipList.append(item['sourceIp'])
            nodes.append({ 
            "Id": item['sourceIp'],
            "name": item['hostName'],
            "ip": item['sourceIp'],
            "dataType": item['protocol']
            })

        if item['destinationIp'] not in ipList:
            ipList.append(item['destinationIp'])
            nodes.append({ 
            "Id": item['destinationIp'],
            "name": item['hostName'],
            "ip": item['destinationIp'],
            "dataType": item['protocol']
            })

    return nodes

def create_routeOpt_structure(json_file):
    routeOpt = {}
    routeOpt["links"] = add_routeOpt_links_data(json_file)
    routeOpt["nodes"] = add_routeOpt_nodes_data(json_file)

    return routeOpt

def create_roa_stucture(json_file, node_data):
    roa_structure = {}
    roa_structure["links"] = add_links_data_roa(json_file)
    roa_structure["nodes"] = add_nodes_data_roa(json_file)
    roa_structure["raGroup"] = add_ragroup_data_roa(roa_structure["links"])
    roa_structure["routeOpt"] = create_routeOpt_structure(json_file)

    return roa_structure