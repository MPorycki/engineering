from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema

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

