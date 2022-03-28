def add_links_applications_hosts(response_data):
    for app in response_data[0]["app"]:
        for host in range(app["hosts"]):
            link_dict = {
            "color": "#0000FF",
            "source": "",
            "target": "",
            "typeConnect":"ASYNC",
            "value":0
            }
            link_dict["source"] = app["name"]
            link_dict["target"] = "host " + str( host + 1)
            response_data[0]["links"].append(link_dict)
            for cluster in response_data[0]["clusters"]:
                if cluster["id"] == app["clusterID"]:
                    cluster["links"].append(link_dict)


def add_links_hosts_services(response_data):
    for service in response_data[0]["services"]:
        link_dict = {
            "color": "#0000FF",
            "source": "",
            "target": "",
            "typeConnect":"ASYNC",
            "value":0
            }
        link_dict["source"] ="host " +str(service["hostID"])
        link_dict["target"] = service["ip"] + ":" + service["containerPort"]
        response_data[0]["links"].append(link_dict)
        for cluster in response_data[0]["clusters"]:
            if service["appID"] == cluster["id"]:
                cluster["links"].append(link_dict)


def add_links_hosts_datasets(response_data):
    for dataset in response_data[0]["datasets"]:
        link_dict = {
            "color": "#0000FF",
            "source": "",
            "target": "",
            "typeConnect":"ASYNC",
            "value":0
            }
        link_dict["source"] ="host " + str(dataset["hostName"])
        link_dict["target"] = dataset["ip"] + ":" + dataset["containerPort"]
        response_data[0]["links"].append(link_dict)
        for cluster in response_data[0]["clusters"]:
            if dataset["appID"] == cluster["id"]:
                cluster["links"].append(link_dict)