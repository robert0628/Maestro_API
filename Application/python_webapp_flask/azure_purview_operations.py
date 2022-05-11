collection_operations = [
    'create_or_update',
    'create_or_update_bulk',
    'move_entities_to_collection'
]

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
discovery_operations = [
    'auto_complete',
    'browse',
    'query',
    'suggest'
]

relationship_operations = [
    'get',
    'create',
    'update',
    'delete'
]

lineage_operations = [
    'get_lineage_graph',
    'next_page_lineage'
]

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