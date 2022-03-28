import json

def vm_recommendation(response_data, initial_data):
    dic_nodes = {}
    for node in response_data[0]["nodes"]:
        if "clusterID" in node:
            if not node["clusterID"] in dic_nodes.keys():
                dic_nodes.update({node["clusterID"]: [] })
            dic_nodes[node["clusterID"]].append(node["id"])

    dic_cluster_traffic = {}
    dic_recommendations = {}
    dic_conditions = {}
    with open("specs.json" ,'r') as g:
        specs = json.load(g)
        for item in specs["Items"]:
            if not float(item["RAM"].split(" ")[0]) in dic_conditions.keys():
                dic_conditions.update({float(item["RAM"].split(" ")[0]) : []})
            dic_conditions[float(item["RAM"].split(" ")[0])].append(item["armskuName"])
    traffic = 0
    for cluster in dic_nodes:
        for ip in dic_nodes[cluster]:      
            val = ip.split(":")   
            for entry in initial_data['items']:
                if val[0] in entry["sourceIp"]:
                    traffic = traffic + int(entry["bytesSent"])
        dic_cluster_traffic[cluster] = traffic
    min_unit_price = 10000
    min_vm_name = ""
    for cluster in dic_cluster_traffic:
        for entry in dic_conditions:
            if dic_cluster_traffic[cluster] < entry*1024:
                with open("specs.json" ,'r') as file:
                    data = json.load(file)
                    for item in data["Items"]:
                        for key in dic_conditions:
                            if item["armskuName"] in dic_conditions[key]:
                                if item["retailPrice"] < min_unit_price:
                                    min_unit_price = item["retailPrice"]
                                    min_vm_name = item["armskuName"]
        dic_recommendations[cluster] = (min_unit_price, min_vm_name)
    with open("specs.json", 'r') as f:
        data = json.load(f)
        for item in data["Items"]:
            for cluster in dic_recommendations:
                if item["armskuName"] in dic_recommendations[cluster]:
                    dic_recommendations[cluster] = item

    hardware_recommendations_response = []
    for key in dic_recommendations:
        element_dict = {}
        for cluster in response_data[0]["clusters"]:
            if cluster["id"] == key:
                element_dict["CurrentDeviceName"] = " "
                element_dict["clusterID"] = cluster["id"]
                element_dict["Azure"] = [dic_recommendations[key]]
                element_dict["CurrentDeviceFunction"] = " "
                element_dict["CurrentDeviceType"] = "Server"
        if not element_dict:
            continue
        hardware_recommendations_response.append(element_dict)
    
    return hardware_recommendations_response