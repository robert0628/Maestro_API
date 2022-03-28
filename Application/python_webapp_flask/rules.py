import json

def rule1(cand_nodes, edges, threshold):
    _edges = list(set(edges))
    inbound_connections = {}
    for edge in _edges:
        key = edge.split(",")[1]
        if key not in inbound_connections:
            inbound_connections[key] = 1
        else:
            inbound_connections[key] += 1
    for k, v in inbound_connections.items():
        if v >= threshold:
            cand_nodes.append(k)
    return cand_nodes


def get_ip_protocol_list(s_port, service_dict, port_dict):
    temp_list = []
    if s_port in service_dict:
        for protocol, description in service_dict[s_port]:
            for ip in port_dict:
                for port in port_dict[ip]:
                    if s_port == port:
                        ip_port_protocol = (f"{ip}" + ":" + f"{port}", protocol)
                        temp_list.append(ip_port_protocol)
    return temp_list

def rule2(cand_nodes, edges):
    service_dict = {}
    with open('port_mapping.json', 'r') as json_file:
        service_dict = json.load(json_file)

    for key in service_dict["ports"]:
        val = service_dict["ports"][key]
        if isinstance(val, list):
            val = val[0]
        port = val["port"]
        protocol = ""
        if val["tcp"]:
            if val["udp"]:
                protocol = "tcp/udp"
            else:
                protocol = "tcp"
        elif val["udp"]:
            protocol = "udp"
        else:
            protocol = "Unofficial"
        description = val["description"]
        if port not in service_dict:
            service_dict[port] = [(protocol, description)]
        else:
            service_dict[port].append((protocol, description))


    port_dict = {}

    for edge in edges:
        destination = edge.split(",")[1]
        dest_ip, port  = destination.split(":")

        if dest_ip not in port_dict:
            port_dict[dest_ip] = [port]
        else:
            if port not in port_dict[dest_ip]:
                port_dict[dest_ip].append(port)

    cand_nodes = []
    for s_port in service_dict["ports"]:
        temp_list = get_ip_protocol_list(s_port, service_dict, port_dict)
        if len(temp_list):
            if len(cand_nodes):
                for dict_ in cand_nodes:
                    for name, dic_ in dict_.items():
                        if(description != name):
                            description_dict = {}
                            description_dict[description] = temp_list
                            cand_nodes.append(description_dict)
                        else:
                            new_list = dic_
                            for item in temp_list:
                                new_list.append(item)
            else:
                description_dict = {}
                description_dict[description] = temp_list
                cand_nodes.append(description_dict)
    return(cand_nodes)

def rule3(cand_nodes, edges, threshold):
    connection_rate = {}
    for edge in edges:
        destination = edge.split(",")[1]
        for node in cand_nodes:
            if destination == node:
                if node not in connection_rate:
                    connection_rate[node] = 1
                else:
                    connection_rate[node] += 1
    cand_nodes_copy = []
    connection_rate_copy = {}
    for k, v in connection_rate.items():
        if v > threshold:
            cand_nodes_copy.append(k)
            connection_rate_copy[k] = v
    return cand_nodes_copy, connection_rate_copy

def select_microservice(json_file, which):
    edges = []

    for obj in json_file['items']:
        ip0 = obj['sourceIp']  # sender
        port0 = obj['sourcePort']
        node_s = ip0[:-1] + ":" + str(port0)

        ip1 = obj['destinationIp']  # receiver
        port1 = obj['destinationPort']
        node_d = ip1[:-1] + ":" + str(port1)

        edge = node_s + "," + node_d
        edges.append(edge)

    cand_nodes1 = rule1([], edges, 2)

    if(which > 0 and which < 4):
        if(which == 1):
            return cand_nodes1
        elif(which == 2):
            cand_nodes2 = rule2(cand_nodes1, edges)
            return cand_nodes2
        elif(which == 3):
            cand_nodes3, rates = rule3(cand_nodes1, edges, 1)
            return cand_nodes3
    else:
        return cand_nodes1

def apply_separation_rule(response_data):
    max_connections = 0

    for data in response_data:
        for ip in data["nodes"]:
            for connections in data["links"]:
                if(connections["target"] == ip["id"] or connections["source"] == ip["id"]):
                    ip["connections"] += 1
                    if(ip["connections"] > max_connections):
                        max_connections = ip["connections"]
                    if(connections["target"] == ip["id"]):
                        ip["incoming"] += 1
                    if(connections["source"] == ip["id"]):
                        ip["outgoing"] += 1
                if(connections["source"] == ip["id"]):
                    ip["outgoing"] += 1

    return response_data

def apply_rule2(response_data, rule2):
    data_name = "information"
    for _dict in rule2:
        for services in _dict:
            for info in _dict[services]:
                for i in range(len(response_data)):
                    for j in range(len(response_data[i]["nodes"])):
                        if(response_data[i]["nodes"][j]["id"] == info[0]):
                            try:
                                old_data = []
                                if(type(response_data[i]["nodes"][j][data_name]) != 'list'):
                                    old_data.append(response_data[i]["nodes"][j][data_name])
                                    old_data.append(info[1])
                                else:
                                    old_data.append(info[1])
                                response_data[i]["nodes"][j][data_name] = old_data
                            except:
                                response_data[i]["nodes"][j][data_name] = info[1]
    return response_data