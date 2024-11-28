from flask_restx import Api
from flask import Blueprint
from .main.controller.testcase_controller import api as testcase_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Customer dashboard',
          version='1.0',
          description=''
          )

api.add_namespace(testcase_ns, path='/testcase-gen')
