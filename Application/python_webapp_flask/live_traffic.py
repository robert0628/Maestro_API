import html
import requests
import datetime
from colour import Color
from netaddr import IPNetwork
from .RCAA_functions import generate_token

networks_url = 'https://71.25.48.227/api/fmc_config/v1/domain/{}/object/networks?limit=1000&expanded=true'

def get_networks():
    accesstoken, refreshtoken, DOMAIN_UUID = generate_token()

    headers = {
        'accept' : 'application/json',
        'X-auth-access-token': accesstoken
    }

    networks_response = requests.get(networks_url.format(DOMAIN_UUID), verify = False, headers = headers)
    networks_response = networks_response.json()

    return networks_response

def get_subnets():
    networks_response = get_networks()
    networks = {}

    for item in networks_response['items']:
        addresses = []
        addr, mask = item['value'].split('/')

        #TODO:find a better way to filter
        if mask != '24':
            continue
        
        network = IPNetwork(item['value'])
        generator = network.iter_hosts()
        for elem in generator:
            addresses.append(str(elem))
        
        networks[item['value']] = addresses
    return networks
    
def auto_graph_generate_nodes(nodes, json_file):
    incoming_data = outgoing_data = incoming_connections = outgoing_connections = {}

    for item in json_file['items']:
        if item['destinationIp'] not in incoming_data.keys():
            incoming_data[item['destinationIp']] = item['bytesSent']
            incoming_connections[item['destinationIp']] = 0 
        else:
            incoming_data[item['destinationIp']] += item['bytesSent']
            incoming_connections[item['destinationIp']] +=  1

        if item['sourceIp'] not in outgoing_data.keys():
            outgoing_data[item['sourceIp']] = item['bytesSent']
            outgoing_connections[item['sourceIp']] = 0 
        else:
            outgoing_data[item['sourceIp']] += item['bytesSent']
            outgoing_connections[item['sourceIp']] += 1
            
    return convert_nodes(nodes=nodes, items=json_file['items'], incoming_data=incoming_data, incoming_connections=incoming_connections, outgoing_data=outgoing_data, outgoing_connections=outgoing_connections)

def convert_nodes(nodes, items, incoming_data, incoming_connections, outgoing_data, outgoing_connections):
    networks = get_subnets()
    for node in nodes:
        keys = ['connections', 'incoming', 'outgoing', 'svg']
        for key in keys:
            del node[key]

        node['status'] = "online"
        node['ip'] = node['id']
        node['id'] = 'HostUUID'
        #we can't get hostUUID as of now

        node['nodeName'] = protocol = sourcePort = node['macAddress'] = ''
        
        for item in items:
            if item['sourceIp'] == node['ip']:
                node['macAddress'] = item['srcMAC']
                protocol = item['protocol']
                sourcePort = item['sourcePort']
                if node['nodeName'] == '':
                    node['nodeName'] = item['hostName']
            if item['destinationIp'] == node['ip']:
                node['macAddress'] = item['dstMAC']

        addresses = get_ips(node['ip'])

        lst_ip = addresses[0].split('.') #TODO
        lst_ip[-1] = '0'

        node['ip_scope'] = '.'.join(lst_ip)
        node['ipGateway'] = addresses[0]

        node['networkGroup'] = ''

        for net in networks.keys():
            if node['ip'] in networks[net]:
                node['networkGroup'] = net

        if node['ip'] in incoming_data.keys():
            node['l_incomingData'] = incoming_data[node['ip']]
            node['l_incomingConn'] = incoming_connections[node['ip']]
        else:
            node['l_incomingData'] = 0
            node['l_incomingConn'] = 0

        if node['ip'] in outgoing_data.keys():
            node['l_outgoingData'] = outgoing_data[node['ip']]
            node['l_outgoingConn'] = outgoing_connections[node['ip']]
        else:
            node['l_outgoingData'] = 0
            node['l_outgoingConn'] = 0

        try:
            sourcePort = int(sourcePort)
        except:
            sourcePort = ''

        node = set_device_data(node, protocol, sourcePort)

    return nodes

def get_ips(ip):
    addresses = []
    network = IPNetwork('/'.join([ip, '24']))
    #TODO:find proper mask
    generator = network.iter_hosts()
    for elem in generator:
        addresses.append(str(elem))
    return addresses

def set_device_data(node, protocol, sourcePort):
    node['port'] = {
            "id": "protocoPortObjUUID",
            "name": "protocolport_obj",
            "type": "ProtocolPortObject",
            "protocol": protocol,
            "port": sourcePort
          }

    if (node['l_outgoingConn'] == 0 and node['l_incomingConn'] > 0 and node['l_outgoingData'] == 0):
        objectType = 'Server'
    else:
        objectType = 'Client'

    node['objectType'] = objectType #TODO
    node['os'] = ''
    node['domain'] = ''
    node['deviceDetails'] = {
        "cpuType": "unknown",
        "cpuCores": "unknown",
        "memoryInMB": "unknown",
        "storageInGB": "unknown"
    }
    node['geo'] = {
        "name": "geolocation",
        "type": "Geolocation",
        "id": "geolocationUUID",
    }
    return node

def live_graph_generate_nodes(nodes, json_file):
    return auto_graph_generate_nodes(nodes, json_file)

def parse_traffic_line(line):
    line = " ".join(line.split())
    splits = line.split(" ")
    has_port = True
    index = splits[0]
    timestap = splits[1]
    source = splits[2].split(".")
    source_ip = source[0]+"."+source[1]+"."+source[2]+"."+source[3]
    source_port = 0
    upd_length = 0
    if "udp" in line:
        upd_length = int(line[line.find("udp")+4:])
    try:
        source_port = source[4]
    except IndexError:
        has_port = False

    destination = splits[4].split(".")
    destination_ip = destination[0]+"."+destination[1]+"."+destination[2]+"."+destination[3]
    destination_port = 0
    try:
        destination_port = destination[4]
    except IndexError:
        has_port = False

    return has_port, index, timestap, (source_ip, source_port), (destination_ip, destination_port), upd_length

def convert_to_json(content):
    data = content["response"][0]
    data = html.unescape(data)
    with open("live_data.txt", "w") as f:
        f.write(data)

    file_handle = open("live_data.txt")
    file_handle.readline()
    captured_packets_str = file_handle.readline()
    file_handle.readline()
    file_it = reversed(list(file_handle))
    next(file_it)
    json_file = {"items":[]}

    for line in file_it:
        has_port, index, timestamp, source, destination, udp_length = parse_traffic_line(line.rstrip())
        if not has_port:
            continue
        source_ip, source_port = source
        destination_ip, destination_port = destination
        dt = datetime.datetime.strptime(timestamp, "%H:%M:%S.%f").timetuple()
        sec, min, hour = dt.tm_sec, dt.tm_min, dt.tm_hour

        json_file["items"].append({
            "index": index,
            "sourceIp": source_ip,
            "sourcePort": source_port,
            "destinationIp": destination_ip,
            "destinationPort": destination_port,
            "second": sec,
            "minute": min,
            "hour": hour,
            "udpLength": udp_length
        })
    file_handle.close()
    return json_file

def transf_to_interval(value, max_value, a=1, b=100):
    if max_value == 0:
        return a
    return int(a + value / max_value * (b-a))

def colour_gradient(colour1, colour2, range):
    start = Color(colour1)
    colours = list(start.range_to(Color(colour2), range))

    return colours

def process_data(response_data, live_data, timeframe=10000):
    temp_links = {}

    for line in live_data["items"]:
        sourceIp, destinationIp = line["sourceIp"], line["destinationIp"]
        if f"{sourceIp}.{destinationIp}" not in temp_links:
            temp_links[f"{sourceIp}_{destinationIp}"] = line["bytesSent"]
        else:
            temp_links[f"{sourceIp}_{destinationIp}"] += line["bytesSent"]

    max_udp_length = 0
    for link in response_data["links"]:
        known_traffic = False
        for ip_key, udp_length in temp_links.items():
            source = ip_key.split("_")[0]
            target = ip_key.split("_")[1]
            if link["source"] == source and link["target"] == target:
                if udp_length > max_udp_length:
                    max_udp_length = udp_length
                link["value"] = udp_length
                known_traffic = True
                break
        if known_traffic is False:
            link["value"] = 0
    return response_data, max_udp_length

def process_auto_graph_data(response_data, live_data, timeframe=10000):
    response_data, max_udp_length = process_data(response_data, live_data, timeframe)

    for link in response_data["links"]:
        if link["value"] > 0:
            link['trafficType'] = 'TCP'
            #TODO:there's multiple types of traffic for IP1:IP2 connection ???
            link['absolutePath'] = [link['source'], link['target']]
        del link['value']

    return response_data

def process_live_data(response_data, live_data, timeframe=10000):
    response_data, max_udp_length = process_data(response_data, live_data, timeframe)

    for link in response_data["links"]:
        if link["value"] > 0:
            link["CurrentTafficSize"] = link["value"]
            link["value"] = transf_to_interval(link["value"], max_udp_length)
            link['trafficType'] = 'TCP'
            #TODO:there's multiple types of traffic for IP1:IP2 connection ???
            link['absolutePath'] = [link['source'], link['target']]

    for el in response_data["links"]:
        if el["value"] < 50:
            colour_gradient_list = colour_gradient("#008000", "#ff0", 50)
            el["color"] = colour_gradient_list[el["value"]].hex
        else:
            colour_gradient_list = colour_gradient("#ff0", "#f00", 50)
            el["color"] = colour_gradient_list[el["value"] - 1 - 50].hex

    return response_data