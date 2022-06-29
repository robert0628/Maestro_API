from .updating_links import *
from .rules import *
from .live_traffic import *
from .process_nodes import *
from .user_interface import *
from .data_insight import *
from .app_rationalization import *
from .RCAA_functions import *
from .update_nodes import *
from .util import *
from vm_recommendations import vm_recommendation


def resolve_livegraph(obj, info):
    try:

        json_file = json.load(open('generated.json'))
        response_data = [get_nodes(json_file, False, [])]
        response_data.append(get_ui_element(response_data))
        response_data[1]["ObjectType"] = generate_ui_techknow(response_data)

        outside_changes_color(response_data[0])
        process_live_data(response_data[0], json_file)

        response_data[0]["nodes"] = live_graph_generate_nodes(response_data[0]["nodes"], json_file)

        for el in response_data[0]["links"]:
            if el["value"] < 50:
                colour_gradient_list = colour_gradient("#00FF00", "#FFFF00", 50)
                el["color"] = colour_gradient_list[el["value"]].hex
            else:
                colour_gradient_list = colour_gradient("#FFFF00", "#FF0000", 50)
                el["color"] = colour_gradient_list[el["value"] - 1 - 50].hex
        
        

        payload = {
            "success": True,
            "links": response_data[0]["links"],
            "nodes": response_data[0]["nodes"]
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload



def resolve_autograph(obj, info):
    try:

        json_file = json.load(open('generated.json'))
        response_data = [get_nodes(json_file, False, [])]
        response_data.append(get_ui_element(response_data))
        response_data[1]["ObjectType"] = generate_ui_techknow(response_data)

        process_auto_graph_data(response_data[0], json_file)

        response_data[0]["nodes"] = auto_graph_generate_nodes(response_data[0]["nodes"], json_file)

        payload = {
            "success": True,
            "links": response_data[0]["links"],
            "nodes": response_data[0]["nodes"]
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload



def resolve_app_rationalization(obj, info, limit=None):
    try:
        limit = limit if limit else 1000

        response = create_app_rationalization_stucture(page_size=limit)
        payload = {
            "success": True,
            "applications": response['applications']
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

def resolve_hardware_2_cloud(obj, info):
    try:
        
        initial_data = json.load(open('generated.json'))
        response_data = generate_mono_2_micro()
        applications, services, hosts, databases, groups = augment_data(response_data[0]["nodes"],response_data[0]["links"])
        response_data[0]["clusters"] = groups
        response = vm_recommendation(response_data, initial_data)
        payload = {
            "success": True,
            "h2c": response
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_containerization_model(obj, info):
    try:
        
        data = generate_mono_2_micro()
        clusters = get_clusters(data[0]["nodes"])      
        response = get_contain(clusters)
        payload = {
            "success": True,
            "cm": response
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload