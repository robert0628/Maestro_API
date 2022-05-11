from queue import Empty
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

def purview_catalog_entity(operation, data):
    client = purview_client()
    entity = client.entity

    response = {}

    if data is None:
        data = {}

    entity_operations = [
        'add_classification',
        'add_classifications',
        'add_classifications_by_unique_attribute',
        'create_or_update',
        'create_or_update_entities',
        'delete_by_guid',
        'delete_by_guids',
        'delete_by_unique_attribute',
        'delete_classification',
        'delete_classification_by_unique_attribute',
        'get_by_guid',
        'get_by_unique_attributes',
        'get_classification',
        'get_classifications',
        'get_entities_by_unique_attributes',
        'get_header',
        'list_by_guids',
        'partial_update_entity_attribute_by_guid',
        'partial_update_entity_by_unique_attributes',
        'set_classifications',
        'update_classifications',
        'update_classifications_by_unique_attribute'
    ]

    if operation in entity_operations:
        pass
    else:
        response["Error"] = "operation not Supported!"
        return response

    if operation == 'add_classification':
            try:
                # Associate a classification to multiple entities in bulk.
                classification_obj = data
                entities_add_classification = entity.add_classification(classification_obj)
                response = entities_add_classification
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'add_classifications':
            try:
                # Add classifications to an existing entity represented by a GUID.
                entity_guid = data
                classifications_list = data
                entity_add_classifications = entity.add_classifications(entity_guid, classifications_list)
                response = entity_add_classifications
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'add_classifications_by_unique_attribute':
            try:
                # Add classification to the entity identified by its type and unique attributes.
                name = data
                classifications_list = data
                entity_add_classifications_by_attr = entity.add_classifications_by_unique_attribute(name, classifications_list)
                response = entity_add_classifications_by_attr
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'create_or_update':
            try:
                # Create or update an entity in Atlas. Existing entity is matched using its unique guid if supplied or by its unique attributes eg: qualifiedName.   
                entity_obj = data
                entity_create_update = entity.create_or_update(entity_obj)
                response = entity_create_update
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'create_or_update_entities':
            try:
                # Create or update entities in Atlas in bulk
                entities_obj = data
                entity_create_or_update_bulk = entity.create_or_update_entities(entities_obj)
                response = entity_create_or_update_bulk
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'delete_by_guid':
            try:
                # Delete an entity identified by its GUID.
                entity_guid = data
                entity_delete = entity.delete_by_guid(entity_guid)
                response = entity_delete
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'delete_by_guids':
            try:
                # Delete a list of entities in bulk identified by their GUIDs or unique attributes.
                entities_list = data
                entity_delete_bulk = entity.delete_by_guids(entities_list)
                response = entity_delete_bulk
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'delete_by_unique_attribute':
            try:
                # Delete an entity identified by its type and unique attributes.
                entity_type_name = data
                entity_classification_delete_by_attr = entity.delete_by_unique_attribute(entity_type_name)
                response = entity_classification_delete_by_attr
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'delete_classification':
            try:
                # Delete a given classification from an existing entity represented by a GUID.
                entity_guid = data
                classification_name = data # Classification name
                entity_classification_delete = entity.delete_classification(entity_guid, classification_name)
                response = entity_classification_delete
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'delete_classification_by_unique_attribute':
            try:
                # Delete a given classification from an entity identified by its type and unique attributes.
                entity_type_name = data # TypeName
                classification_name = data # Classification name
                entity_classification_delete_by_attr = entity.delete_classification_by_unique_attribute(entity_type_name, classification_name)
                response = entity_classification_delete_by_attr
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'get_by_guid':
            try:
                # Get complete definition of an entity given its GUID.
                entity_guid = data
                entity_details = entity.get_by_guid(entity_guid)
                response = entity_details
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'get_by_unique_attributes':
            try:
                # Get complete definition of an entity given its type and unique attribute. In addition to the typeName path parameter, attribute key-value pair(s) can be provided ex.
                # GET /v2/entity/uniqueAttribute/type/aType?attr:aTypeAttribute=someValue.
                entity_type_name = data
                entity_details_by_unique_attr = entity.get_by_unique_attributes(entity_type_name)
                response = entity_details_by_unique_attr
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'get_classification':
            try:
                # List classification of a given entity represented by a GUID.
                classification_guid = data
                classification_name = data
                entity_get_classification = entity.get_classification(classification_guid, classification_name)
                response = entity_get_classification
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'get_classifications':
            try:
                # List classifications for a given entity represented by a GUID.
                classification_guid = data
                entity_get_classifications = entity.get_classifications(classification_guid)
                response = entity_get_classifications
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'get_entities_by_unique_attributes':
            try:
                # Bulk API to retrieve list of entities identified by its unique attributes.
                entity_type_name = data
                entities_details_by_unique_attr = entity.get_entities_by_unique_attributes(entity_type_name)
                response = entities_details_by_unique_attr
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'get_header':
            try:
                # Get entity header given its GUID.
                entity_guid = data
                entity_get_header = entity.get_header(entity_guid)
                response = entity_get_header
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'list_by_guids':
            try:
                # List entities in bulk identified by its GUIDs.
                entities_list = data
                entities_details = entity.list_by_guids(entities_list)
                response = entities_details
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'partial_update_entity_attribute_by_guid':
            try:
                # Update entity partially - create or update entity attribute identified by its GUID. Supports only primitive attribute type and entity references.
                entity_guid = data
                attr_obj = data
                entity_partial_update_attr = entity.partial_update_entity_attribute_by_guid(entity_guid, attr_obj)
                response = entity_partial_update_attr
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'partial_update_entity_by_unique_attributes':
            try:
                # Update entity partially - Allow a subset of attributes to be updated on an entity which is identified by its type and unique attribute eg: Referenceable.qualifiedName.
                entity_type_name = data
                entity_obj = data
                entity_partial_update_by_attr = entity.partial_update_entity_by_unique_attributes(entity_type_name, entity_obj)
                response = entity_partial_update_by_attr
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'set_classifications':
            try:
                # Set classifications on entities in bulk.
                entity_headers_obj = data
                entity_set_classifications_bulk = entity.set_classifications(entity_headers_obj)
                response = entity_set_classifications_bulk
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'update_classifications':
            try:
                # Update classifications to an existing entity represented by a guid.
                entity_guid = data
                classifications_list = data
                entity_update_classifications = entity.update_classifications(entity_guid, classifications_list)
                response = entity_update_classifications
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'update_classifications_by_unique_attribute':
            try:
                # Update classification on an entity identified by its type and unique attributes.
                entity_type_name = data
                classifications_list = data
                entity_update_classifications_by_attr = entity.update_classifications_by_unique_attribute(entity_type_name, classifications_list)
                response = entity_update_classifications_by_attr
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response

def purview_catalog_glossary(operation, data):
    client = purview_client()
    glossary = client.glossary

    response = {}

    if data is None:
        data = ""
    if data is None:
        data = {}
    glossary_operations = [
        'assign_term_to_entities',
        'begin_import_glossary_terms_via_csv',
        'begin_import_glossary_terms_via_csv_by_glossary_name',
        'create_glossary',
        'create_glossary_categories',
        'create_glossary_category',
        'create_glossary_term',
        'create_glossary_terms',
        'delete_glossary',
        'delete_glossary_category',
        'delete_glossary_term',
        'delete_term_assignment_from_entities',
        'export_glossary_terms_as_csv',
        'get_detailed_glossary',
        'get_entities_assigned_with_term',
        'get_glossary',
        'get_glossary_category',
        'get_glossary_term',
        'get_import_csv_operation_status',
        'list_category_terms',
        'list_glossaries',
        'list_glossary_categories',
        'list_glossary_categories_headers',
        'list_glossary_term_headers',
        'list_glossary_terms',
        'list_related_categories',
        'list_related_terms',
        'list_terms_by_glossary_name',
        'partial_update_glossary',
        'partial_update_glossary_category',
        'partial_update_glossary_term',
        'remove_term_assignment_from_entities',
        'update_glossary',
        'update_glossary_category',
        'update_glossary_term'
    ]

    if operation in glossary_operations:
        pass
    else:
        response["Error"] = "operation not Supported!"
        return response

    if operation == 'getAll':
            try:
                # Get all Glossaries in Purview Atlas.
                glossary_get_all = glossary.list_glossaries()
                response = glossary_get_all
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'assignTermToEntities':
            try:
                # Assign the given term to the provided list of related dataects.
                term_guid = data
                related_object_ids = data
                glossary_assign_term_to_entities = glossary.assign_term_to_entities(term_guid, related_object_ids)
                response = glossary_assign_term_to_entities
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'createCategory':
            try:
                # Create a glossary category.
                glossary_category = data
                glossary_create_category = glossary.create_glossary_category(glossary_category)
                response = glossary_create_category
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'createCategories':
            try:
                # Create glossary category in bulk.
                glossary_category = data
                glossary_create_categories_bulk = glossary.create_glossary_categories(glossary_category)
                response = glossary_create_categories_bulk
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'getDetails':
            try:
                # Get a specific glossary with detailed information by guid.
                glossary_guid = data
                glossary_detailed_by_guid = glossary.get_detailed_glossary(glossary_guid)
                response = glossary_detailed_by_guid
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'get':
            try:
                # Get a specific Glossary by its GUID.
                glossary_guid = data
                glossary_by_guid = glossary.get_glossary(glossary_guid)
                response = glossary_by_guid
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'getCategory':
            try:
                # Get specific glossary category by its GUID.
                category_guid = data
                glossary_category_by_guid = glossary.get_glossary_category(category_guid)
                response = glossary_category_by_guid
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'getEntitiesFromTerm':
            try:
                # Get all related objects assigned with the specified term.
                term_guid = data
                glossary_entities_assigned_with_term = glossary.get_entities_assigned_with_term(term_guid)
                response = glossary_entities_assigned_with_term
                return response            
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'getCategories':
            try:
                # Get the categories belonging to a specific glossary.
                glossary_guid = data
                glossary_get_categories = glossary.list_glossary_categories(glossary_guid)
                response = glossary_get_categories
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'getTerm':
            try:
                # Get a specific glossary term by its GUID.
                term_guid = data
                glossary_term_by_guid = glossary.get_glossary_term(term_guid)
                response = glossary_term_by_guid
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'getTermsByGlossaryName':
            try:
                # Get terms by glossary name.
                glossary_name = data
                glossary_terms_by_name = glossary.list_terms_by_glossary_name(glossary_name)
                response = glossary_terms_by_name
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'getTerms':
            try:
                # Get terms belonging to a specific glossary.
                glossary_guid = data
                glossary_get_terms = glossary.list_glossary_terms(glossary_guid)
                response = glossary_get_terms
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'getCategoryTerms':
            try:
                # Get all terms associated with the specific category.
                category_guid = data
                glossary_category_terms = glossary.list_category_terms(category_guid)
                response = glossary_category_terms
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'getCategoriesHeaders':
            try:
                # Get the category headers belonging to a specific glossary.
                glossary_guid = data
                glossary_get_categories_headers = glossary.list_glossary_categories_headers(glossary_guid)
                response = glossary_get_categories_headers
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'getTermHeaders':
            try:
                # Get term headers belonging to a specific glossary.
                glossary_guid = data
                glossary_get_term_headers = glossary.list_glossary_term_headers(glossary_guid)
                response = glossary_get_term_headers
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'getRelatedCategories':
            try:
                # Get all related categories (parent and children). Limit, offset, and sort parameters are currently not being enabled and won’t work even they are passed.
                category_guid = data
                glossary_related_categories = glossary.list_related_categories(category_guid)
                response = glossary_related_categories
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'getTermsFromTerm':
            try:
                # Get all related terms for a specific term by its GUID. Limit, offset, and sort parameters are currently not being enabled and won’t work even they are passed.
                term_guid = data
                glossary_term_related_terms = glossary.list_related_terms(term_guid)
                response = glossary_term_related_terms
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'createTerm':
            try:
                # Create a glossary term.
                glossary_term = data
                glossary_create_term = glossary.create_glossary_term(glossary_term)
                print(glossary_create_term)
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'createTerms':
            try:
                # Create glossary terms in bulk.
                glossary_terms = data
                glossary_create_terms_bulk = glossary.create_glossary_terms(glossary_terms)
                print(glossary_create_terms_bulk)
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'delete':
            try:
                # Delete a glossary.
                glossary_guid = data
                glossary_delete = glossary.delete_glossary(glossary_guid)
                print(glossary_delete)
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response                
    elif operation == 'deleteCategory':
            try:
                # Delete a glossary category.
                category_guid = data
                glossary_delete_category = glossary.delete_glossary_category(category_guid)
                print(glossary_delete_category)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response                
    elif operation == 'deleteTerm':
            try:
                # Delete a glossary term.
                term_guid = data
                glossary_delete_term = glossary.delete_glossary_term(term_guid)
                print(glossary_delete_term)
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response                
    elif operation == 'deleteTermFromEntities':
            try:
                # Delete a glossary term from entities.
                term_guid = data
                related_object_ids = data
                glossary_delete_term_from_entities = glossary.delete_term_assignment_from_entities(term_guid, related_object_ids)
                print(glossary_delete_term_from_entities)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'exportTermsToCSV':
            try:
                # Export glossary terms as CSV
                glossary_guid = data
                term_guids = data
                glossary_export_terms_csv = glossary.export_glossary_terms_as_csv(glossary_guid, term_guids)
                print(glossary_export_terms_csv)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'updatePartial':
            try:
                # Update the glossary partially. Some properties such as qualifiedName are not allowed to be updated.
                glossary_guid = data
                partial_updates = data
                glossary_update_partial = glossary.partial_update_glossary(glossary_guid, partial_updates)
                print(glossary_update_partial)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response                
    elif operation == 'updateCategoryPartial':
            try:
                # Update the glossary category partially.
                category_guid = data
                partial_updates = data
                glossary_update_category_partial = glossary.partial_update_glossary_category(category_guid, partial_updates)
                print(glossary_update_category_partial)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response                
    elif operation == 'updateTermPartial':
            try:
                # Update the glossary term partially.
                term_guid = data
                partial_updates = data
                glossary_update_term_partial = glossary.partial_update_glossary_term(term_guid, partial_updates)
                print(glossary_update_term_partial)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'deleteTermFromEntities':
            try:
                # Delete the term assignment for the given list of related objects.
                term_guid = data
                related_object_ids = data
                glossary_delete_term_from_entities = glossary.remove_term_assignment_from_entities(term_guid, related_object_ids)
                print(glossary_delete_term_from_entities)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'update':
            try:
                # Update the given glossary.
                glossary_guid = data
                updated_glossary = data
                glossary_update = glossary.update_glossary(glossary_guid, updated_glossary)
                print(glossary_update)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'updateCategory':
            try:
                # Update the given glossary category by its GUID.
                category_guid = data
                glossary_category = data
                glossary_update_category = glossary.update_glossary_category(category_guid, glossary_category)
                print(glossary_update_category)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response
    elif operation == 'updateTerm':
            try:
                # Update the given glossary term by its GUID.
                term_guid = data
                glossary_term = data
                glossary_update_term = glossary.update_glossary_term(term_guid, glossary_term)
                print(glossary_update_term)
                
                return response
            except HttpResponseError as err:
                response["Error"] = err
                return response

def purview_catalog_discovery(operation, data):
    client = purview_client()
    discovery = client.discovery
    response = {}

    if data is None:
        data = ""
    if data is None:
        data = {}
    discovery_operations = [
        'auto_complete',
        'browse',
        'query',
        'suggest'
    ]

    if operation in discovery_operations:
        pass
    else:
        response["Error"] = "operation not Supported!"
        return response
    try:
        if data is not None:
            getattr(discovery, operation)(data)
        else:
            getattr(discovery, operation)()
    except HttpResponseError as err:
            response["Error"] = err
            return response
    # if operation == 'autocomplete':
    #         try:
    #             # Get auto complete options. Requires as parameter a JSON object specifying the autocomplete criteria.
    #             auto_complete_criteria = data

    #             discovery_auto_complete = discovery.auto_complete(auto_complete_criteria)
    #             response = discovery_auto_complete
    #             return response
    #         except HttpResponseError as err:
    #             response["Error"] = err
    #             return response
    # elif operation == 'browse':
    #         try:
    #             # Browse entities by path or entity type.
    #             browse_entity = data

    #             discovery_browse = discovery.browse(browse_entity)
    #             response = discovery_browse
    #             return response
    #         except HttpResponseError as err:
    #             response["Error"] = err
    #             return response
    # elif operation == 'query':
    #         try:
    #             # Gets data using search with a JSON object specifying the search criteria.
    #             search_criteria = data
                
    #             discovery_search = discovery.query(search_criteria)
    #             response = discovery_search
    #             return response
    #         except HttpResponseError as err:
    #             response["Error"] = err
    #             return response
    # elif operation == 'suggest':
    #         try:
    #             # Get search suggestions by query criteria with a JSON object specifying the suggest criteria.
    #             suggest_criteria = data
    #             discovery_suggest = discovery.suggest(suggest_criteria)
    #             response = discovery_suggest
    #             return response
    #         except HttpResponseError as err:
    #             response["Error"] = err
    #             return response                                

def purview_catalog_lineage(operation, data):
    client = purview_client()
    lineage = client.lineage
    response = {}

    if data is None:
        data = {}
    lineage_operations = [
        'get_lineage_graph',
        'next_page_lineage'
    ]
    if operation in lineage_operations:
        pass
    else:
        response["Error"] = "operation not Supported!"
        return response

    if operation == 'get_lineage_graph':
        try:
            # Get lineage info of the entity specified by GUID.
            lineage_guid = data

            lineage_get_graph = lineage.get_lineage_graph(lineage_guid, direction="BOTH")
            response = lineage_get_graph
            return response
        except HttpResponseError as err:
            response["Error"] = err
            return response
    elif operation == 'next_page_lineage':
        try:
            # Return immediate next page lineage info about entity with pagination.
            lineage_guid = data

            lineage_next_page = lineage.next_page_lineage(lineage_guid)
            response = lineage_next_page
            return response
        except HttpResponseError as err:
            response["Error"] = err
            return response

def purview_catalog_relationship(operation, data):
    client = purview_client()
    relationship = client.relationship
    response = {}

    if data is None:
        data = {}

    relationship_operations = [
        'get',
        'create',
        'update',
        'delete'
    ]

    if operation in relationship_operations:
        pass
    else:
        response["Error"] = "operation not Supported!"
        return response
    try:
        if data is not None:
            getattr(relationship, operation)(data)
        else:
            getattr(relationship, operation)()
    except HttpResponseError as err:
            response["Error"] = err
            return response


    # if operation == 'get':
    #     try:
    #         # Get relationship information between entities by its GUID.  
    #         relationship_guid = data
    #         relationship_get = relationship.get(relationship_guid)
    #         response = relationship_get
    #         return response
    #     except HttpResponseError as err:
    #         response["Error"] = err
    #         return response
    # elif operation == 'create':
    #     try:
    #         # Create a new relationship between entities.
    #         relationship_obj = data
    #         relationship_create = relationship.create(relationship_obj)
    #         response = relationship_create
    #         return response
    #     except HttpResponseError as err:
    #         response["Error"] = err
    #         return response
    # elif operation == 'update':
    #     try:
    #         # Return immediate next page lineage info about entity with pagination.
    #         relationship_obj = data
    #         relationship_update = relationship.update(relationship_obj)
    #         response = relationship_update
    #         return response
    #     except HttpResponseError as err:
    #         response["Error"] = err
    #         return response            
    # elif operation == 'delete':
    #     try:
    #         # Delete a relationship between entities by its GUID.
    #         relationship_guid = data
    #         relationship_delete = relationship.delete(relationship_guid)
    #         response = relationship_delete
    #         return response


def purview_catalog_types(operation, data):
    client = purview_client()
    types = client.types
    response = {}

    if data is None:
        data = {}

    types_operations = [
        'create_type_definitions',
        'delete_type_by_name',
        'delete_type_definitions',
        'get_all_type_definitions',
        'get_classification_def_by_guid',
        'get_classification_def_by_name',
        'get_entity_definition_by_guid',
        'get_entity_definition_by_name',
        'get_enum_def_by_guid',
        'get_enum_def_by_name',
        'get_relationship_def_by_guid',
        'get_relationship_def_by_name',
        'get_struct_def_by_guid',
        'get_struct_def_by_name',
        'get_term_template_def_by_guid',
        'get_term_template_def_by_name',
        'get_type_definition_by_guid',
        'get_type_definition_by_name',
        'list_type_definition_headers',
        'update_type_definitions'
    ]

    if operation in types_operations:
        pass
    else:
        response["Error"] = "operation not Supported!"
        return response

    if operation == 'get_all_type_definitions':
        try:
            # Get all type definitions.
            get_all_types = types.get_all_type_definitions()
            
            response = get_all_types
            return response
        except HttpResponseError as err:
            response["Error"] = err
            return response
    elif operation == 'create_or_update':
        try:
            # Creates or updates entities in bulk to a collection. Existing entity is matched using its unique guid if supplied or by its unique attributes eg: qualifiedName.
            collection_name = data
            collection_entity_to_update = data
            collection_update = types.create_or_update(collection_name, collection_entity_to_update)

            response = collection_update
            return response
        except HttpResponseError as err:
            response["Error"] = err
            return response            
    elif operation == 'createUpdateEntitiesIn':
        try:
            # Creates or updates entities in bulk to a collection. Existing entity is matched using its unique guid if supplied or by its unique attributes eg: qualifiedName.
            collection_name = data
            collection_entities_to_update = data
            collection_update = types.create_or_update_bulk(collection_name, collection_entities_to_update)

            response = collection_update
            return response
        except HttpResponseError as err:
            response["Error"] = err
            return response

def purview_catalog_collection(operation, data):
    client = purview_client()
    collection = client.collection

    response = {}

    if data is None:
        data = ""
    if data is None:
        data = {}
    collection_operations = [
        'create_or_update',
        'create_or_update_bulk',
        'move_entities_to_collection'
    ]

    if operation in collection_operations:
        pass
    else:
        response["Error"] = "operation not Supported!"
        return response

    try:
        pass
    except HttpResponseError as err:
        return err

    # if operation == 'create_or_update':
    #     try:
    #         # Creates or updates an entity to a collection. Existing entity is matched using its unique guid if supplied or by its unique attributes eg: qualifiedName.
    #         collection_name = data
    #         collection_entity_to_update = data
    #         collection_create = collection.create_or_update(collection_name, collection_entity_to_update)
    #         response = collection_create
    #         return response
    #     except HttpResponseError as err:
    #         response["Error"] = err
    #         return response
    # elif operation == 'create_or_update_bulk':
    #     try:
    #         # Creates or updates entities in bulk to a collection. Existing entity is matched using its unique guid if supplied or by its unique attributes eg: qualifiedName.
    #         collection_name = data
    #         collection_entities_to_update = data
    #         collection_update = collection.create_or_update_bulk(collection_name, collection_entities_to_update)

    #         response = collection_update
    #         return response
    #     except HttpResponseError as err:
    #         response["Error"] = err
    #         return response
    # elif operation == 'move_entities_to_collection':
    #     try:
    #         # Move existing entities to the target collection.
    #         collection_name = data
    #         collection_move_entitites = data

    #         collection_move_entities = collection.move_entities_to_collection(collection_name, collection_move_entitites)

    #         response = collection_move_entities
    #         return response
    #     except HttpResponseError as err:
    #         response["Error"] = err
    #         return response
