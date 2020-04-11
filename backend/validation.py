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
