from azure.purview.catalog import PurviewCatalogClient
from azure.identity import ClientSecretCredential

tenantId = "ababe4b8-e9ca-48b1-910a-9a632c08bff2"
clientId = "d7b2cf84-1728-4ebc-a7ed-f2a4f1fa8dfe"
clientSecret = "a~Z8Q~i5zsaWLO5.HdPtxRSWNpyMaquqWadP7ajQ"
acc_name = "democui"

def purview_client():
    credential = ClientSecretCredential(tenantId, clientId, clientSecret)
    client = PurviewCatalogClient(endpoint="https://{}.purview.azure.com".format(acc_name), credential=credential)
    return client

def purview_catalog():
    client = purview_client()
    try:
        response = client.types.get_all_type_definitions()
        # print out all of your entity definitions
        return response
    except err as err:
        print(err)