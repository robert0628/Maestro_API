from scapy.all import *
import json
import math
from datetime import datetime

import datetime


def convert_size(size_bytes):
    if size_bytes < (1024 / 2 - 1):
       return "0 KB"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p)
    return "%s %s" % (s, size_name[i])

def get_pcap_summary(pkt):
    item = {}
    hostname = ""
    if 'Ethernet' in pkt:
            item['srcMAC'] = pkt['Ethernet'].src
            item['dstMAC'] = pkt['Ethernet'].dst
    if 'NBT Datagram Packet' in pkt:
        hostname = pkt['NBT Datagram Packet'].SourceName
        try:
            hostname = pkt['NBT Datagram Packet'].SourceName.decode('utf-8')
        except:
            hostname = ""
    if 'IP' in pkt:
        ip_src = pkt['IP'].src
        ip_dst = pkt['IP'].dst
        bytes_sent = len(pkt)
        item['sourceIp'] = ip_src
        item['destinationIp'] = ip_dst
        item['bytesSent'] = bytes_sent

        if 'TCP' in pkt:
            tcp_sport = pkt['TCP'].sport
            tcp_dport = pkt['TCP'].dport

            item['protocol'] = 'TCP'
            item['sourcePort'] = str(tcp_sport)
            item['destinationPort'] = str(tcp_dport)

        if 'UDP' in pkt:
            udp_sport = pkt['UDP'].sport
            udp_dport = pkt['UDP'].dport

            item['protocol'] = 'UDP'
            item['sourcePort'] = str(udp_sport)
            item['destinationPort'] = str(udp_dport)        
        
        # date_time = datetime.datetime.fromtimestamp(float(pkt.time))
        # item['timeReceived'] = str(date_time)

        item["hostName"] = hostname

        try:
            sourceIp = item['sourceIp']
            destinationIp = item['destinationIp']
            sourcePort = item['sourcePort']
            destinationPort = item['destinationPort']
            return item
        except:
            return 0
    return 0

def pkg_to_json(packet):
    packet_dict = {}

    for line in packet.show2(dump=True).split('\n'):
        if '###' in line:
            layer = line.strip('#[] ')
            packet_dict[layer] = {}
        elif '=' in line:
            key, val = line.split('=', 1)
            packet_dict[layer][key.strip()] = val.strip()

    return json.dumps(packet_dict)

def pcap_to_json(pcap_file_path):
    packets = rdpcap(pcap_file_path)
    packets_list = []

    for packet in packets:
        elem = get_pcap_summary(packet)
        if elem != 0 and elem not in packets_list:
            packets_list.append(elem)

    json_item = {}
    json_item['items'] = packets_list

    return json_item

def pcaps_to_json(pcap_files_path):
    final_json = {}
    final_json['items'] = []
    
    for path in pcap_files_path:
        print(path)
        json_item = pcap_to_json(path)
        final_json['items'].extend(json_item['items'])

    return final_json

def generate_json():
    filenames = [
        "pcap_0.pcap",
        "pcap_1.pcap",
        "pcap_2.pcap",
        "pcap_3.pcap",
        "pcap_4.pcap",
        "pcap_5.pcap",
    ]
    json_obj = pcaps_to_json(filenames)
    with open('generated.json', 'w') as file:
        json.dump(json_obj, file, indent = 4)