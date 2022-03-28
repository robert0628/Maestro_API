def create_navbar_data(node_connections, max_edges, response_data):
    computer_svg = "RiComputerLine"
    printer_svg = "RiPrinterLine"
    json_connections = {
        "clusters":[]
    }
    for i in range(1, max_edges):
        number = len(json_connections["clusters"]) + 1
        name = "Cluster " + str(number)

        json_temp = {
            "Name":name,
            "Components":[]
        }
        for connections in node_connections:
            if(len(connections[1]) == i):
                temp_list = []
                temp_list.append(connections[0])
                temp_list.extend(connections[1])

                head = None
                icons_list = []

                for temp_node in temp_list:
                    node = None
                    for given_node in response_data["nodes"]:
                        if(temp_node == given_node["id"]):
                            node = given_node
                            break
                    if(node["incoming"] == node["cluster"] or node["outgoing"] == node["cluster"]):
                        head = node["id"]
                        temp_list.remove(head)
                        break
                    icons_list.append(printer_svg)

                if head == None:
                    head = connections[0]

                json_temp2 = {
                    "Parent":head,
                    "parentIcon":computer_svg,
                    "Child":temp_list,
                    "childIcon":icons_list,
                }
                json_temp["Components"].append(json_temp2)
        if(len(json_temp["Components"])):
            json_connections["clusters"].append(json_temp)
    return json_connections

def set_specific_icons(response_data):
    server = "https://www.svgrepo.com/show/1296/student-computer.svg"
    printer = "https://www.svgrepo.com/show/34160/printer.svg"

    for node in response_data["nodes"]:
        if(node["connections"] == node["cluster"]):
            if(node["cluster"] > 0):
                node["svg"] = server
            else:
                node["svg"] = printer
        else:
            node["svg"] = printer
    return response_data

def create_template_new_node(counter, cluster, svg, elem, port):
    return  {
        "id": counter,
        "groupID": cluster,
        "status": "online",
        "ep_icon": svg,
        "name": elem["id"],
        "ip": elem["id"].split(":")[0],
        "ports": port
    }

def create_template_cluster(i, cluster):
    return {
           "id":  i,
           "image": chr(i + 64),
           "name": cluster["Name"]
    }

def get_ui_element(data, json_connections = 0):
    navbar = ""
    response_data = {}

    if(json_connections == 0):
        prev_data = data[0]
        response_data = {
            "UI-Interface": []
        }
    else:
        response_data = {
            "UI-Interface": [],
            "groups": [],
            "ObjectType": []
        }
        prev_data = data
        navbar = json_connections["clusters"]

    nodes = []
    counter = 0
    for elem in prev_data["nodes"]:
        try:
            counter += 1
            cluster = ""
            svg = ""
            port = ""    
            try:
                cluster = elem["cluster"] - 1
                svg = elem["svg"]
                port = elem["id"].split(":")[1]
            except:
                pass

            new_node = create_template_new_node(counter, cluster, svg, elem, port)

            if(new_node["ports"] == ""):
                del new_node["ports"]
            if(new_node["ep_icon"] == ""):
                del new_node["ep_icon"]
            if(new_node["groupID"] == ""):
                del new_node["groupID"]

            if(not new_node["name"].startswith("Cluster")):
                nodes.append(new_node)
        except:
            pass
    response_data["UI-Interface"] = nodes

    if(navbar != ""):
        groups = []
        i = 1
        for cluster in navbar:
            group_obj = create_template_cluster(i, cluster)
            groups.append(group_obj)
            i += 1
        response_data["groups"] = groups

    ObjectType = []

    children = []
    for elem in prev_data["nodes"]:
        try:
            if(elem["svg"].rsplit("/",1)[1].split(".")[0] == "student-computer"):
                new_dict = {
                    "id": elem["index"] + 1,
                    "name": elem["id"]
                }
                children.append(new_dict)
        except:
            pass
    Servers = {
        "category": "Servers",
        "child": children
    }

    if(len(Servers["child"])):
        ObjectType.append(Servers)

    children = []
    for elem in prev_data["nodes"]:
        try:
            if(elem["svg"].rsplit("/",1)[1].split(".")[0] == "printer"):
                new_dict = {
                    "id": elem["index"] + 1,
                    "name": elem["id"]
                }
                children.append(new_dict)
        except:
            pass
    Clients = {
        "category": "Clients",
        "child": children
    }
    if(len(Clients["child"])):
        ObjectType.append(Clients)

    if(len(Clients["child"]) or len(Servers["child"])):
        response_data["ObjectType"] = ObjectType
    return response_data

def generate_ui_techknow(response_data):
    objectTypeJson = [{"category": "Servers", "child": []}, {"category": "Clients", "child": []}]

    idx_server, idx_client = 0, 0
    for item in response_data[0]["nodes"]:
        if item["incoming"] > 2:
            objectTypeJson[0]["child"].append({ "id": idx_server, "name": "Server " + str(idx_server)})
            idx_server += 1
        else:
            objectTypeJson[1]["child"].append({ "id": idx_client, "name": "Client " + str(idx_client)})
            idx_client += 1
    return objectTypeJson