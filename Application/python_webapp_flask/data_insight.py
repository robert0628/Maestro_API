import json
import random 

threshold_tier1 = 3
threshold_tier2 = 10
threshold_tier3 = 20

def get_clusters(nodes):
    clusters = {}
    if nodes is not None:
        for node in nodes:
            try:
                if node["groupID"] != 0: # only consider servers
                    ip, port = node["id"].split(":")
                    if node["clusterID"] not in clusters:
                        clusters[node["clusterID"]] = [{"ip": ip, "port": port, "requests": node["groupID"]}]
                    else:
                        if node["id"] not in clusters[node["clusterID"]]: # enforce correction
                            clusters[node["clusterID"]].append({"ip": ip, "port": port, "requests": node["groupID"]})
            except KeyError:
                continue

    return clusters

def get_k8s_resources(requests):
    if requests <= threshold_tier1:
        cpu_requests, memory_requests = "250m", "128Mi"
        cpu_limits, memory_limits = "500m", "256Mi"
    elif threshold_tier1 < requests <= threshold_tier2:
        cpu_requests, memory_requests = "500m", "256Mi"
        cpu_limits, memory_limits = "725m", "512Mi" 
    else:
        cpu_requests, memory_requests = "725m", "512Mi"
        cpu_limits, memory_limits = "1000m", "1024Mi" 
    return cpu_limits, memory_limits, cpu_requests, memory_requests

def get_ids(nodes):
    servers_ids, idx1 = {}, 0
    host_ids, idx2 = {}, 0
    if nodes is not None:
        for node in nodes:
            try:
                if node["groupID"] != 0: # only consider servers
                    if node["id"] not in servers_ids:
                        idx1 += 1
                        servers_ids[node["id"]]=idx1
                    ip = node["id"].split(":")[0]
                    if ip not in host_ids:
                        idx2 += 1
                        host_ids[ip]=idx2
            except KeyError:
                continue
 
    return servers_ids, host_ids
 
def app_json(clusterID, complexScore, n_services, n_datasets, n_hosts, dependent):
    return {
        "id": clusterID,
        "clusterID": clusterID,
        "name": f"app {clusterID}",
        "complexScore": complexScore,
        "size":  random.randint(2, 50), #TO-DO: change this in the future to reflect real app size
        "services": n_services, 
        "datasets": n_datasets, 
        "dependent": dependent,
        "hosts":n_hosts
    }
 
def service_json(serviceID, appID, ip, port, cpu_limits, memory_limits, cpu_requests, memory_requests, hostName):
    return {
        "id": serviceID,
        "appID": appID,
        "ip": ip,
        "name": f"service {serviceID}",
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
        "hostID": hostName
    }
 
def host_json(hostName, appID, serviceID, cpu_limits, memory_limits, cpu_requests, memory_requests):
    return {
        "id": hostName,
        "appID": appID, 
        "serviceID": serviceID, 
        "name": f"host {hostName}",
        "resources": {
            "limits": {
                "cpu": cpu_limits,
                "memory": memory_limits
            },
            "requests": {
                "cpu": cpu_requests,
                "memory": memory_requests
            }
        }
    }

def database_json(appID, hostName, serviceID, ip, port, cpu_limits, memory_limits, cpu_requests, memory_requests):
    return {
        "appID": appID,
        "id" : hostName,
        "containerPort": port,
        "hostName": hostName,
        "ip": ip,
        "name": f"dataset {appID}",
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
        "id": serviceID,
    }

def group_json(clusterID, containers, nodes, links, services, hosts, applications, databases):
    return {
        "id": clusterID,
        "name": f"Cluster {clusterID}",
        "nodes": group_nodes_by_cluster_id(clusterID, nodes),
        "links": group_links_by_cluster_id(containers, links),
    }

def group_applications_by_cluster_id(clusterID, applications):
    return [application for application in applications if application["clusterID"]==clusterID]

def group_databases_by_cluster_id(clusterID, databases):
    return [database for database in databases if database["appID"]==clusterID]

def group_services_by_cluster_id(clusterID, services):
    return [service for service in services if service["appID"]==clusterID]

def group_hosts_by_cluster_id(clusterID, hosts):
        return [host for host in hosts if host["appID"]==clusterID]

def group_nodes_by_cluster_id(clusterID, nodes):
    return [node for node in nodes if node["clusterID"]==clusterID]

def group_links_by_cluster_id(containers, links):
    services = [container["ip"]+":"+container["port"] for container in containers]
    return [link for link in links if link["source"] in services or link["target"] in services]        
        
def group_by_cluster_id(clusters, nodes, links, services, hosts, applications, databases):
    groups = []
    for clusterID, containers in clusters.items():
        groups.append(group_json(clusterID, containers, nodes, links, services, hosts, applications, databases))
    return groups

def compute_complexity(requests):
    if requests < threshold_tier1:
        return 25
    elif threshold_tier1 <= requests < threshold_tier2:
        return 50
    elif threshold_tier2 <= requests < threshold_tier3:
        return 75
    else:
        return 100

def get_db_ports():
    dbs = json.load(open('python_webapp_flask/db_ports.json'))["commonDBs"]
    db_ports = []
    [db_ports.extend(db["ports"]) for db in dbs]
    return db_ports

def count_service_types(containers, db_ports):
    n_services, n_datasets, n_hosts, dependent = 0, 0, 0, 0
    hosts = []
    for container in containers:
        ip, port = container["ip"], container["port"]
        if ip not in hosts:
            hosts.append(ip)
        if port in db_ports:
            n_datasets += 1
        else:
            n_services += 1
    n_hosts = len(hosts)
    dependent = n_services + n_datasets    
    return n_services, n_datasets, n_hosts, dependent 

def add_categories(nodes, databases, services):
    for node in nodes:
        appID = 0
        category = "Not Found"
        for el in databases:
            if str(el["ip"]) == str(node["id"]).split(':')[0]:
                appID = el["appID"]
                category = "dataset"
        for el in services:
            if el["ip"] == str(node["id"]).split(':')[0]:
                appID = el["appID"]
                category = "service"
        node["appID"] = appID
        node["category"] = category
    return nodes

def check_app(appID, applications):
    appIDs = [app["clusterID"] for app in applications]
    return appID in appIDs


def augment_data(nodes, links):
    clusters = get_clusters(nodes)
    service_ids, host_ids = get_ids(nodes)
    applications, services, hosts, databases, groups = [], [], [], [], []
    db_ports = get_db_ports()
    for clusterID, containers in clusters.items():
        for container in containers:
            cpu_limits, memory_limits, cpu_requests, memory_requests = get_k8s_resources(container["requests"]) 
            id = container["ip"]+":"+container["port"]
            hostName = host_ids[container["ip"]]
            complexScore = compute_complexity(container["requests"])
            n_services, n_datasets, n_hosts, dependent = count_service_types(containers, db_ports)
            if not check_app(clusterID, applications):
                applications.append(app_json(clusterID, complexScore, n_services, n_datasets, n_hosts, dependent))
            services.append(service_json(service_ids[id], clusterID, container["ip"], container["port"], 
                                         cpu_limits, memory_limits, cpu_requests, memory_requests, hostName))
            hosts.append(host_json(hostName, clusterID, service_ids[id], cpu_limits, 
                                   memory_limits, cpu_requests, memory_requests))
            if container['port'] in db_ports:
                databases.append(database_json(clusterID, hostName, service_ids[id], container["ip"], container["port"], cpu_limits, 
                                               memory_limits, cpu_requests, memory_requests))
    nodes = add_categories(nodes, databases, services)
    groups = group_by_cluster_id(clusters, nodes, links, services, hosts, applications, databases)
    return applications, services, hosts, databases, groups
    