from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

# https://python-jsonschema.readthedocs.io/en/stable/
# https://json-schema.org/draft-07/json-schema-validation.html#rfc.section.3.2.1


visit_schema = {
    'type': 'object',
    'properties': {
        'hairdresser_id': {
            'type': 'string',
            'pattern': r'^[a-f0-9]{32}$'
        },
        'salon_id': {
            'type': 'string',
        },
        'visit_date_start': {
            'type': 'string',
        },
        'service_duration': {
            'type': 'number',
        },
        'services': {
            'type': "array"
        }
    },
    'required': ['hairdresser_id', 'salon_id',
                 'visit_date_start', 'service_duration', 'services']
}


class VisitInputs(Inputs):
    json = [JsonSchema(schema=visit_schema)]
