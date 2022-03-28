from .RCAA_functions import *

fmc_api_applications = 'https://71.25.48.227/api/fmc_config/v1/domain/{}/object/applications?limit=1000&expanded=true'
fmc_api_domain_information = 'https://71.25.48.227/api/fmc_platform/v1/info/domain'
fmc_api_sla_monitors = 'https://71.25.48.227/api/fmc_config/v1/domain/{}/object/slamonitors?limit=1000&expanded=true'

productivity_mapping = {
  'VERY_LOW': 1, 
  'LOW': 2,
  'MEDIUM': 2.5,
  'HIGH': 4.5,
  'VERY_HIGH': 5
}

risk_mapping = {
  'VERY_LOW': 1, 
  'LOW': 2,
  'MEDIUM': 2.5,
  'HIGH': 4.5,
  'VERY_HIGH': 5
}

def create_application_item(data):
    try:

      applicationTypes = '';
      description = '';
      productivity = ''

      if 'applicationTypes' in data.keys():
        for el_type in data['applicationTypes']:
          applicationTypes += el_type['name'] + '|'

        applicationTypes = applicationTypes[:-1]

      if 'appCategories' in data.keys():
        for el_category in data['appCategories']:
          description += el_category['name'] + '|'

        description = description[:-1]

      appProductivity = data['appProductivity']['id']
      appProductivity = productivity_mapping[appProductivity]

      appRisk = data['risk']['id']
      appRisk = risk_mapping[appRisk]

      #TODO:we can't obtain appsize we can only estimate it
      appSize = 64*appProductivity

      element = {
        "name": data['name'],
        "appId": data['appId'],
        "appIP": "0.0.0.0",
        "appSize": str(appSize) + " MBs",
        "description": description,
        "applicationTypes": applicationTypes,
        "productivity": appProductivity,
        "***risk": appRisk,
        "***riskScore": str(appRisk),
        "DCIM_tools": "",
        "data_management_systems": "",
        "hardware_tracking_systems": "",
        "SLA_trend": "",
        "virtualization_management_system": "",
        "technical_requirements_bandwidth": "",
        "technical_requirements_data": " ",
        "scalability_adaptability": " ",
        "security_standards": " ",
        "dependencies_upstream_identity": " ",
        "dependencies_downstream_identity": " ",
        "duplication": "false",
        "supportEstCost": "",
        "powerExpense": "",
        "hosting_options": "",
        "migration_scale": str(appProductivity*2+appRisk*2)#TODO:create formula for this
        }

      return element

    except Exception as e:
      print('[ERROR]Failed to parse data in create_application_item')
      return {}


def app_rationalization_add_items(accesstoken, DOMAIN_UUID):
    all_applications = []

    headers = {
        'accept' : 'application/json',
        'X-auth-access-token': accesstoken
    }

    applications_api = fmc_api_applications.format(DOMAIN_UUID)
    sla_monitor_api = fmc_api_sla_monitors.format(DOMAIN_UUID)

    response = requests.get(applications_api, verify = False, headers = headers)
    application_dict = response.json()

    if len(application_dict['items']) == 0:
      return items

    for item in application_dict['items']:
      all_applications.append(create_application_item(item))

    return all_applications

def create_app_rationalization_stucture():

    accesstoken, refreshtoken, DOMAIN_UUID = generate_token()

    app_rationalization_structure = {}
    app_rationalization_structure["applications"] = app_rationalization_add_items(accesstoken, DOMAIN_UUID)

    return app_rationalization_structure
