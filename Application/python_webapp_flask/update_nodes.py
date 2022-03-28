def add_apps_nodes(response_data):
    for app in response_data[0]["app"]:
        node_dict={
        "appID": 0,
        "category": "",
        "clusterID": 0,
        "containerID": 0,
        "groupID": 0,
        "id": "",
        "port": ""
        }

        node_dict["appID"] = app["id"]
        node_dict["category"] = "app"
        node_dict["clusterID"] = app["clusterID"]
        node_dict["id"] = app["id"]
        response_data[0]["nodes"].append(node_dict)

        for cluster in response_data[0]["clusters"]:
            if app["clusterID"] == cluster["id"]:
                cluster["nodes"].append(node_dict)

def add_hosts_nodes(response_data):
    for host in response_data[0]["hosts"]:
        node_dict={
        "appID": 0,
        "category": "",
        "clusterID": 0,
        "containerID": 0,
        "groupID": 0,
        "id": "",
        "port": ""
        }
        
        node_dict["appID"] = host["appID"]
        node_dict["category"] = "host"
        node_dict["clusterID"] = host["appID"]
        node_dict["id"] = host["id"]
        response_data[0]["nodes"].append(node_dict)

        for cluster in response_data[0]["clusters"]:
            if host["appID"] == cluster["id"]:
                cluster["nodes"].append(node_dict)