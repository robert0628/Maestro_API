from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML

from flask import Blueprint,request, jsonify

from python_webapp_flask import queries

module = Blueprint('index',
    __name__,
    url_prefix=''
)


query = ObjectType("Query")
query.set_field("livegraph", queries.resolve_livegraph)
query.set_field("autograph", queries.resolve_autograph)
query.set_field("app_rationalization", queries.resolve_app_rationalization)
query.set_field("hardware_2_cloud", queries.resolve_hardware_2_cloud)
query.set_field("containerization_model", queries.resolve_containerization_model)
query.set_field("rcaa", queries.resolve_rcaa)
query.set_field("mono_2_micro", queries.resolve_mono_2_micro)




type_defs = load_schema_from_path("graphQL_schema")

type_defs = [
    load_schema_from_path("schema.graphql"),
    load_schema_from_path("graphQL_schema"),
]
schema = make_executable_schema(
    type_defs, query
)
@module.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@module.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code