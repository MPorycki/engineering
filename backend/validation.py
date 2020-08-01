from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

# https://python-jsonschema.readthedocs.io/en/stable/
# https://json-schema.org/draft-07/json-schema-validation.html#rfc.section.3.2.1

service_schema = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string'
        },
        'price': {
            'type': 'number'
        },
        'description': {
            'type': 'string'
        },
        'gender': {
            'type': 'string'
        },
        'service_duration': {
            'type': 'number'
        }
    },
    'required': ['name', 'price', 'description', 'gender', 'service_duration']
}


class ServiceInputs(Inputs):
    json = [JsonSchema(schema=service_schema)]


salon_schema = {
    'type': 'object',
    'properties': {
        'opening_hour': {
            'type': 'string',
            'pattern': r'[0-9]{2}:[0-9]{2}'
        },
        'closing_hour': {
            'type': 'string',
            'pattern': r'[0-9]{2}:[0-9]{2}'
        },
        'adress': {
            'type': 'object',
        },
    },
    'required': ['opening_hour', 'closing_hour', 'adress']
}


class SalonInputs(Inputs):
    json = [JsonSchema(schema=salon_schema)]


visit_schema = {
    'type': 'object',
    'properties': {
        'customer_id': {
            'type': 'string',
            'pattern': r'^[a-f0-9]{32}$'
        },
        'hairdresser_id': {
            'type': 'string',
            'pattern': r'^[a-f0-9]{32}$'
        },
        'salon_id': {
            'type': 'string',
        },
        'visit_date_start': {
            'type': 'string',  # TODO add Validation
        },
        'service_duration': {
            'type': 'number',
        },
        'services': {
            'type': "array"
        }
    },
    'required': ['customer_id', 'hairdresser_id', 'salon_id',
                 'visit_date_start', 'service_duration', 'services']
}


class VisitInputs(Inputs):
    json = [JsonSchema(schema=visit_schema)]
