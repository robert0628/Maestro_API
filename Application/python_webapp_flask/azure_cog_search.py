import os
from unittest import skip
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient 
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    ComplexField,
    CorsOptions,
    SearchIndex,
    ScoringProfile,
    SearchFieldDataType,
    SimpleField,
    SearchableField
)


service_name = "nh-inteloo-cog-search"
admin_key = "E35B1A7FDF7983D36945EA94F273AEA4"



def search(search_text = '*', index_name="azureblob-index", page_size=10, page_no=1):
    # Create an SDK client
    endpoint = "https://{}.search.windows.net/".format(service_name)

    search_client = SearchClient(endpoint=endpoint,
                        index_name=index_name,
                        credential=AzureKeyCredential(admin_key))

    results =  search_client.search(search_text=search_text, include_total_count=True, top=page_size, skip=page_size * (page_no-1))

    # print ('Total Documents Matching Query:', results.get_count())

    return results
