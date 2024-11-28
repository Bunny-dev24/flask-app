import traceback
import logging
from flask import request
from flask_restx import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..model.database import get_db
from ..model.customer import Customer
from ..util.dto import CustomerDto

api = CustomerDto.api
customer_model = CustomerDto.customer_model
customer_input_model = CustomerDto.customer_input_model

@api.route('')
class CustomerList(Resource):
    @api.doc('list_all_customers')
    @api.marshal_list_with(customer_model)
    def get(self):
        """Retrieve all customers"""
        try:
            db = next(get_db())
            customers = db.query(Customer).all()
            return [customer.to_dict() for customer in customers]
        except Exception as e:
            logging.error(f"Error listing customers: {str(e)}")
            api.abort(500, f"An error occurred while fetching customers: {str(e)}")

    @api.doc('create_customer')
    @api.expect(customer_input_model)
    @api.marshal_with(customer_model, code=201)
    def post(self):
        """Create a new customer"""
        try:
            db = next(get_db())
            data = request.json

            # Validate required fields
            if not data or not data.get('name') or not data.get('email'):
                api.abort(400, "Name and email are required fields")

            # Check if customer with same email already exists
            existing_customer = db.query(Customer).filter_by(email=data['email']).first()
            if existing_customer:
                api.abort(409, f"Customer with email {data['email']} already exists")

            # Create new customer
            new_customer = Customer(
                name=data['name'],
                email=data['email'],
                phone=data.get('phone', ''),
                address=data.get('address', ''),
                company=data.get('company', '')
            )

            db.add(new_customer)
            db.commit()
            db.refresh(new_customer)

            return new_customer.to_dict(), 201

        except SQLAlchemyError as e:
            db.rollback()
            logging.error(f"Database error creating customer: {str(e)}")
            api.abort(500, f"Database error: {str(e)}")
        except Exception as e:
            db.rollback()
            logging.error(f"Unexpected error creating customer: {str(e)}")
            api.abort(500, f"An unexpected error occurred: {str(e)}")

@api.route('/<int:customer_id>')
@api.param('customer_id', 'The Customer unique identifier')
class CustomerResource(Resource):
    @api.doc('get_customer')
    @api.marshal_with(customer_model)
    def get(self, customer_id):
        """Retrieve a specific customer by ID"""
        try:
            db = next(get_db())
            customer = db.query(Customer).filter_by(id=customer_id).first()
            
            if not customer:
                api.abort(404, f"Customer with ID {customer_id} not found")
            
            return customer.to_dict()
        
        except Exception as e:
            logging.error(f"Error fetching customer {customer_id}: {str(e)}")
            api.abort(500, f"An error occurred while fetching customer: {str(e)}")

    @api.doc('update_customer')
    @api.expect(customer_input_model)
    @api.marshal_with(customer_model)
    def put(self, customer_id):
        """Update an existing customer"""
        try:
            db = next(get_db())
            
            # Find the existing customer
            customer = db.query(Customer).filter_by(id=customer_id).first()
            
            if not customer:
                api.abort(404, f"Customer with ID {customer_id} not found")
            
            # Get update data
            data = request.json

            # Update fields if provided
            if 'name' in data:
                customer.name = data['name']
            if 'email' in data:
                # Check if new email is already in use by another customer
                existing_customer = db.query(Customer).filter(
                    Customer.email == data['email'], 
                    Customer.id != customer_id
                ).first()
                
                if existing_customer:
                    api.abort(409, f"Email {data['email']} is already in use")
                
                customer.email = data['email']
            
            if 'phone' in data:
                customer.phone = data['phone']
            if 'address' in data:
                customer.address = data['address']
            if 'company' in data:
                customer.company = data['company']

            db.commit()
            db.refresh(customer)

            return customer.to_dict()
        
        except SQLAlchemyError as e:
            db.rollback()
            logging.error(f"Database error updating customer: {str(e)}")
            api.abort(500, f"Database error: {str(e)}")
        except Exception as e:
            db.rollback()
            logging.error(f"Unexpected error updating customer: {str(e)}")
            api.abort(500, f"An unexpected error occurred: {str(e)}")

    @api.doc('delete_customer')
    def delete(self, customer_id):
        """Delete a customer"""
        try:
            db = next(get_db())
            
            # Find the customer
            customer = db.query(Customer).filter_by(id=customer_id).first()
            
            if not customer:
                api.abort(404, f"Customer with ID {customer_id} not found")
            
            # Delete the customer
            db.delete(customer)
            db.commit()

            return {'message': f'Customer with ID {customer_id} successfully deleted'}, 200
        
        except SQLAlchemyError as e:
            db.rollback()
            logging.error(f"Database error deleting customer: {str(e)}")
            api.abort(500, f"Database error: {str(e)}")
        except Exception as e:
            db.rollback()
            logging.error(f"Unexpected error deleting customer: {str(e)}")
            api.abort(500, f"An unexpected error occurred: {str(e)}")

@api.route('/search')
class CustomerSearch(Resource):
    @api.doc(params={
        'name': 'Search customer by name (partial match)',
        'email': 'Search customer by email (partial match)',
        'phone': 'Search customer by phone (partial match)'
    })
    @api.marshal_list_with(customer_model)
    def get(self):
        """Search customers by name, email, or phone"""
        try:
            db = next(get_db())
            
            # Get search parameters
            name = request.args.get('name')
            email = request.args.get('email')
            phone = request.args.get('phone')

            # Start with base query
            query = db.query(Customer)

            # Apply filters if parameters are provided
            if name:
                query = query.filter(Customer.name.ilike(f'%{name}%'))
            
            if email:
                query = query.filter(Customer.email.ilike(f'%{email}%'))
            
            if phone:
                query = query.filter(Customer.phone.ilike(f'%{phone}%'))

            # Execute query and return results
            customers = query.all()
            return [customer.to_dict() for customer in customers]
        
        except Exception as e:
            logging.error(f"Error searching customers: {str(e)}")
            api.abort(500, f"An error occurred while searching customers: {str(e)}")