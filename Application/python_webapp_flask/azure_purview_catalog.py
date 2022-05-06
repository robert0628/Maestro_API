from azure.purview.catalog import PurviewCatalogClient
from azure.identity import ClientSecretCredential
from azure.core.exceptions import HttpResponseError

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
    except HttpResponseError as err:
        print(err)

def purview_catalog_entity(entity, obj, guid):
    client = purview_client()
    guid = ""
    entity = ""
    type_name = ""
    attr_qualified_name = ""
    classification_name = ""
    classification = {}
    classifications = []
    classifications_arr = []
    guid_arr = []
    atlas_entity_with_ext_info = {}
    entity_headers = {}
    try:
        # Add classifications to an existing entity represented by a GUID.
        add_classifications_to_entity = client.entity.add_classifications(guid, classifications)

        # Associate a classification to multiple entities in bulk.               
        add_classification_to_multiple_entities = client.entity.add_classification(classification)

        # Add classification to the entity identified by its type and unique attributes.
        add_classifications_by_unique_attr = client.add_classifications_by_unique_attribute(type_name, classifications_arr)

        # Create or update an entity in Atlas. Existing entity is matched using its unique guid if supplied or by its unique attributes eg: qualifiedName.
        entity_create_update =  client.entity.create_or_update(entity)

        # Create or update entities in Atlas in bulk
        entity_create_or_update_bulk = client.entity.create_or_update_entities(entity)

        # Delete an entity identified by its GUID.
        entity_delete = client.entity.delete_by_guid(guid)

        # Delete a list of entities in bulk identified by their GUIDs or unique attributes.
        entity_delete_bulk = client.entity.delete_by_guids(guid_arr)

        # Delete a given classification from an existing entity represented by a GUID.
        entity_classification_delete_by_guid = client.entity.delete_classification(guid, classification_name)
        # Delete a given classification from an entity identified by its type and unique attributes.
        entity_classification_delete_by_unique_attr = client.entity.delete_classification_by_unique_attribute(type_name, classification_name)

        # Get complete definition of an entity given its GUID.
        entity_details_by_guid = client.entity.get_by_guid(guid)

        # Get complete definition of an entity given its type and unique attribute. In addition to the typeName path parameter, attribute key-value pair(s) can be provided ex.
        # GET /v2/entity/uniqueAttribute/type/aType?attr:aTypeAttribute=someValue.
        entity_details_by_unique_attr = client.entity.get_by_unique_attributes(type_name)

        # List classifications for a given entity represented by a GUID.
        entity_classification_by_guid = client.entity.get_classification(guid, classification_name)

        # List classifications for a given entity represented by a GUID.
        entity_classifications_by_unique_attr = client.entity.get_classifications(guid)

        # Bulk API to retrieve list of entities identified by its unique attributes.
        entity_details_bulk_by_unique_attr = client.entity.get_entities_by_unique_attributes(type_name, attr_qualified_name)

        # Get entity header given its GUID.
        entity_get_header_by_guid = client.entity.get_header(guid)

        # List entities in bulk identified by its GUIDs.
        entity_bulk_get_header_by_guid = client.entity.list_by_guids(guid_arr)

        # Update entity partially - create or update entity attribute identified by its GUID
        entity_partial_update_by_guid = client.entity.partial_update_entity_attribute_by_guid(guid)

        #  Update entity partially - Allow a subset of attributes to be updated on an entity which is identified by its type and unique attribute eg: Referenceable.qualifiedName. Null updates are not possible. In addition to the typeName path parameter, attribute key-value pair(s) can be provided.
        entity_partial_update__by_unique_attr = client.entity.partial_update_entity_by_unique_attributes(type_name, atlas_entity_with_ext_info)       

        # Set classifications on entities in bulk.
        entity_set_bulk_classifications = client.entity.set_classifications(entity_headers)

        # Update classifications to an existing entity represented by a guid.
        entity_update_classifications_by_guid = client.entity.update_classifications(guid, classifications)

        # Update classification on an entity identified by its type and unique attributes.
        entity_update_classifications_by_guid = client.entity.update_classifications_by_unique_attribute(type_name, classifications_arr)

        response = {}
        # print out all of your entity definitions
        return response
    except HttpResponseError as err:
        print(err)

def purview_catalog_glossary(action, data, obj):
    client = purview_client()
    glossary = client.glossary

    response = {}

    if data is None:
        data = ""
    if obj is None:
        obj = {}
    glossary_actions = [
        'assignTermToEntities',
        'createCategory',
        'createCategories',
        'createTerm',
        'createTerms',
        'exportTermsToCSV',
        'get',
        'getAll',
        'getDetails',
        'getCategory',
        'getCategoryTerms',
        'getCategories',
        'getTerm',
        'getTerms',
        'getTermsFromTerm',
        'getEntitiesFromTerm',
        'getTermsByGlossaryName',
        'getCategoriesHeaders',
        'getTermHeaders',
        'getRelatedCategories',
        'updateTermPartial',
        'updateCategoryPartial',
        'updatePartial',
        'deleteTermFromEntities',
        'delete',
        'deleteTerm',
        'deleteCategory',
        'update',
        'updateCategory',
        'updateCategoryPartial',
        'updatePartial',
        'updateTerm',
        'updateTermPartial'
    ]

    if action in glossary_actions:
        pass

    if action == 'getAll':
            try:
                # Get all Glossaries in Purview Atlas.
                glossary_get_all = glossary.list_glossaries()
                response = glossary_get_all
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'assignTermToEntities':
            try:
                # Assign the given term to the provided list of related objects.
                term_guid = data
                related_object_ids = obj
                glossary_assign_term_to_entities = glossary.assign_term_to_entities(term_guid, related_object_ids)
                response = glossary_assign_term_to_entities
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'createCategory':
            try:
                # Create a glossary category.
                glossary_category = obj
                glossary_create_category = glossary.create_glossary_category(glossary_category)
                response = glossary_create_category
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'createCategories':
            try:
                # Create glossary category in bulk.
                glossary_category = obj
                glossary_create_categories_bulk = glossary.create_glossary_categories(glossary_category)
                response = glossary_create_categories_bulk
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'getDetails':
            try:
                # Get a specific glossary with detailed information by guid.
                glossary_guid = data
                glossary_detailed_by_guid = glossary.get_detailed_glossary(glossary_guid)
                response = glossary_detailed_by_guid
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'get':
            try:
                # Get a specific Glossary by its GUID.
                glossary_guid = data
                glossary_by_guid = glossary.get_glossary(glossary_guid)
                response = glossary_by_guid
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'getCategory':
            try:
                # Get specific glossary category by its GUID.
                category_guid = data
                glossary_category_by_guid = glossary.get_glossary_category(category_guid)
                response = glossary_category_by_guid
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'getEntitiesFromTerm':
            try:
                # Get all related objects assigned with the specified term.
                term_guid = data
                glossary_entities_assigned_with_term = glossary.get_entities_assigned_with_term(term_guid)
                response = glossary_entities_assigned_with_term
                return response            
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'getCategories':
            try:
                # Get the categories belonging to a specific glossary.
                glossary_guid = data
                glossary_get_categories = glossary.list_glossary_categories(glossary_guid)
                response = glossary_get_categories
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'getTerm':
            try:
                # Get a specific glossary term by its GUID.
                term_guid = data
                glossary_term_by_guid = glossary.get_glossary_term(term_guid)
                response = glossary_term_by_guid
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'getTermsByGlossaryName':
            try:
                # Get terms by glossary name.
                glossary_name = data
                glossary_terms_by_name = glossary.list_terms_by_glossary_name(glossary_name)
                response = glossary_terms_by_name
                return response
            except HttpResponseError as err:
                print(err)
                return "Error"
    elif action == 'getTerms':
            try:
                # Get terms belonging to a specific glossary.
                glossary_guid = data
                glossary_get_terms = glossary.list_glossary_terms(glossary_guid)
                response = glossary_get_terms
                return response
            except HttpResponseError as err:
                response["Error"] = {
                    "message": err.message, 
                    "status": err.status_code
                    }
                return response
    elif action == 'getCategoryTerms':
            try:
                # Get all terms associated with the specific category.
                category_guid = data
                glossary_category_terms = glossary.list_category_terms(category_guid)
                response = glossary_category_terms
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'getCategoriesHeaders':
            try:
                # Get the category headers belonging to a specific glossary.
                glossary_guid = data
                glossary_get_categories_headers = glossary.list_glossary_categories_headers(glossary_guid)
                response = glossary_get_categories_headers
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'getTermHeaders':
            try:
                # Get term headers belonging to a specific glossary.
                glossary_guid = data
                glossary_get_term_headers = glossary.list_glossary_term_headers(glossary_guid)
                response = glossary_get_term_headers
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'getRelatedCategories':
            try:
                # Get all related categories (parent and children). Limit, offset, and sort parameters are currently not being enabled and won’t work even they are passed.
                category_guid = data
                glossary_related_categories = glossary.list_related_categories(category_guid)
                response = glossary_related_categories
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'getTermsFromTerm':
            try:
                # Get all related terms for a specific term by its GUID. Limit, offset, and sort parameters are currently not being enabled and won’t work even they are passed.
                term_guid = data
                glossary_term_related_terms = glossary.list_related_terms(term_guid)
                response = glossary_term_related_terms
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'createTerm':
            try:
                # Create a glossary term.
                glossary_term = obj
                glossary_create_term = glossary.create_glossary_term(glossary_term)
                print(glossary_create_term)
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'createTerms':
            try:
                # Create glossary terms in bulk.
                glossary_terms = obj
                glossary_create_terms_bulk = glossary.create_glossary_terms(glossary_terms)
                print(glossary_create_terms_bulk)
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'delete':
            try:
                # Delete a glossary.
                glossary_guid = data
                glossary_delete = glossary.delete_glossary(glossary_guid)
                print(glossary_delete)
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response                
    elif action == 'deleteCategory':
            try:
                # Delete a glossary category.
                category_guid = data
                glossary_delete_category = glossary.delete_glossary_category(category_guid)
                print(glossary_delete_category)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response                
    elif action == 'deleteTerm':
            try:
                # Delete a glossary term.
                term_guid = data
                glossary_delete_term = glossary.delete_glossary_term(term_guid)
                print(glossary_delete_term)
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response                
    elif action == 'deleteTermFromEntities':
            try:
                # Delete a glossary term from entities.
                term_guid = data
                related_object_ids = obj
                glossary_delete_term_from_entities = glossary.delete_term_assignment_from_entities(term_guid, related_object_ids)
                print(glossary_delete_term_from_entities)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'exportTermsToCSV':
            try:
                # Export glossary terms as CSV
                glossary_guid = data
                term_guids = obj
                glossary_export_terms_csv = glossary.export_glossary_terms_as_csv(glossary_guid, term_guids)
                print(glossary_export_terms_csv)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'updatePartial':
            try:
                # Update the glossary partially. Some properties such as qualifiedName are not allowed to be updated.
                glossary_guid = data
                partial_updates = obj
                glossary_update_partial = glossary.partial_update_glossary(glossary_guid, partial_updates)
                print(glossary_update_partial)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response                
    elif action == 'updateCategoryPartial':
            try:
                # Update the glossary category partially.
                category_guid = data
                partial_updates = obj
                glossary_update_category_partial = glossary.partial_update_glossary_category(category_guid, partial_updates)
                print(glossary_update_category_partial)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response                
    elif action == 'updateTermPartial':
            try:
                # Update the glossary term partially.
                term_guid = data
                partial_updates = obj
                glossary_update_term_partial = glossary.partial_update_glossary_term(term_guid, partial_updates)
                print(glossary_update_term_partial)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'deleteTermFromEntities':
            try:
                # Delete the term assignment for the given list of related objects.
                term_guid = data
                related_object_ids = obj
                glossary_delete_term_from_entities = glossary.remove_term_assignment_from_entities(term_guid, related_object_ids)
                print(glossary_delete_term_from_entities)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'update':
            try:
                # Update the given glossary.
                glossary_guid = data
                updated_glossary = obj
                glossary_update = glossary.update_glossary(glossary_guid, updated_glossary)
                print(glossary_update)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'updateCategory':
            try:
                # Update the given glossary category by its GUID.
                category_guid = data
                glossary_category = obj
                glossary_update_category = glossary.update_glossary_category(category_guid, glossary_category)
                print(glossary_update_category)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif action == 'updateTerm':
            try:
                # Update the given glossary term by its GUID.
                term_guid = data
                glossary_term = obj
                glossary_update_term = glossary.update_glossary_term(term_guid, glossary_term)
                print(glossary_update_term)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response

def purview_catalog_discovery():
    client = purview_client()
    try:
        print(client.discovery)
        response = {}
        # print out all of your entity definitions
        return response
    except HttpResponseError as err:
        print(err)

def purview_catalog_lineage():
    client = purview_client()
    try:
        print(client.lineage)
        response = {}
        # print out all of your entity definitions
        return response
    except HttpResponseError as err:
        print(err)

def purview_catalog_relationship():
    client = purview_client()
    try:
        response = {}
        print(client.relationship)
        # print out all of your entity definitions
        return response
    except HttpResponseError as err:
        print(err)

def purview_catalog_types():
    client = purview_client()
    try:
        response = client.types.get_all_type_definitions()
        # print out all of your entity definitions
        return response
    except HttpResponseError as err:
        print(err)

def purview_catalog_collection():
    client = purview_client()
    try:
        response = {}
        print(client.collection)
        # print out all of your entity definitions
        return response
    except HttpResponseError as err:
        print(err)
