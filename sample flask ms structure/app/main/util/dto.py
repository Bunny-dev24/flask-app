from flask_restx import Namespace, fields

class CustomerDto:
    api = Namespace('customer', description='Customer operations')
    
    customer_model = api.model('Customer', {
        'id': fields.Integer(readonly=True, description='The customer unique identifier'),
        'name': fields.String(required=True, description='Customer full name'),
        'email': fields.String(required=True, description='Customer email address'),
        'phone': fields.String(description='Customer phone number'),
        'address': fields.String(description='Customer address')
    })

    customer_input_model = api.model('CustomerInput', {
        'name': fields.String(required=True, description='Customer full name'),
        'email': fields.String(required=True, description='Customer email address'),
        'phone': fields.String(description='Customer phone number'),
        'address': fields.String(description='Customer address')
    })
