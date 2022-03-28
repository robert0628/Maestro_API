import requests
import json
from datetime import datetime
from requests.auth import HTTPBasicAuth

token_url = 'https://71.25.48.227/api/fmc_platform/v1/auth/generatetoken'

def generate_token():

    response = requests.request("POST", token_url, verify=False, auth=HTTPBasicAuth('labadmin', 'Friday2022!'))

    accesstoken = response.headers["X-auth-access-token"]
    refreshtoken = response.headers["X-auth-refresh-token"]
    DOMAIN_UUID = response.headers["DOMAIN_UUID"]

    return accesstoken, refreshtoken, DOMAIN_UUID

def call_CISCO_fmc_api_incidents_dict():

    accesstoken, refreshtoken, DOMAIN_UUID = generate_token()

    headers = {
        'accept' : 'application/json',
        'X-auth-access-token': accesstoken
    }

    incident_ids = requests.get("https://71.25.48.227/api/fmc_tid/v1/domain/{}/tid/incident".format(DOMAIN_UUID), verify = False, headers = headers)
    incident_dict = incident_ids.json()

    return incident_dict

def call_CISCO_fmc_api_incidents(incidentUUID):
    domain = retrieve_domain()
    try:
        headers = {
            'accept' : 'application/json',
            'X-auth-access-token': 'd31d59ef-1134-4922-800a-958149b40476'
        }
        incident = requests.get("https://71.25.48.227/api/fmc_tid/v1/domain/{}/tid/incident/{}".format(domain, incidentUUID), verify = False, headers = headers)
        return incident.json()
    except:
        return {}

def total_occurences(incident_dict):
    incident_frequency = {}
    try:
        for incidents in incident_dict["Items"]:
            if incidents["id"] in incident_frequency:
                incident_frequency[incidents["id"]] =+ 1
            else:
                incident_frequency[incidents["id"]] = 0
    except:
        print("List is empty")
    return incident_frequency

def alert_status(incident_frequency):
    alert_status_dict = {}
    try:
        for incidents in incident_frequency:
            if incident_frequency[incidents] >= 3 and incident_frequency[incidents] < 5:
                alert_status_dict[incidents] = "Low"
            elif incident_frequency[incidents] >= 5 and incident_frequency[incidents] < 7:
                alert_status_dict[incidents] = "Medium"
            else:
                alert_status_dict[incidents] = "High"
    except:
        print("incident_frequency is empty")
    return alert_status_dict

def build_response(incident_dict):
    RCAA_response = []
    try:
        for incidents in incident_dict["Items"]:
            tmp = {}
            incident = call_CISCO_fmc_api_incidents(incidents["id"])
            incident["updatedAt"] = datetime.fromtimestamp(incident["updatedAt"])
            tmp["sourceName"] = incident["sourcename"]
            tmp["incidentIDs"] = incidents["id"]
            tmp["totalOccurences"] = total_occurences(incident_dict["Items"])[incidents["id"]]
            tmp["alertStatus"] = alert_status(total_occurences(incident_dict["Items"]))[incidents["id"]]
            tmp["Passtrough"] = incident
            RCAA_response.append(tmp)
    except:
        RCAA_response.append(incident_dict)
    return RCAA_response

def return_structure():
    RCAA_response = []
    dict_response = {}
    dict_response["sourceName"] = "sourceName"
    dict_response["incident_ID"] = "incidentUUID"
    dict_response["totalOccurences"] = 0
    dict_response["alertStatus"] = "low"
    dict_response["incidentPassthrough"] ={
    "items":
        {
        "updatedAt": 1499839877,
        "sourceName": "guest.dataForLast_7daysOnly",
        "equation": {
            "children": [
                {
                    "children": [
                        {
                            "isRealized": False,
                            "type": "LL_UNSUPPORTED_OBJECT_TYPE|Port",
                            "value": "IDREF:{http://hailataxii.com}Observable-fc5c11a8-b038-4abc-9641-2b495c78774a"
                        }
                    ],
                    "condition": "EQUALS",
                    "isRealized": False,
                    "applyCondition": "ANY"
                },
                {
                    "children": [
                        {
                            "isRealized": False,
                            "type": "DomainNameObjectType",
                            "value": "domainNameValue"
                        }
                    ],
                    "condition": "EQUALS",
                    "isRealized": False,
                    "applyCondition": "ANY"
                },
                {
                    "children": [
                        {
                            "isRealized": True,
                            "type": "IPV_4_ADDR",
                            "value": "ipAddressValue"
                        }
                    ],
                    "condition": "EQUALS",
                    "isRealized": True,
                    "applyCondition": "ANY"
                }
            ],
            "isRealized": True,
            "op": "OR"
        }
    }
}

    RCAA_response.append(dict_response)
    RCAA_response.append(dict_response)
    return RCAA_response

with open("RCAA_response.json" , 'w') as jsonfile:
    RCAA_response = return_structure()
    json.dump(RCAA_response, jsonfile, indent = 4)