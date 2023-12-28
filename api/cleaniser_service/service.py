from flask import Blueprint

cleanser_service = Blueprint('cleanser_service', __name__)

@cleanser_service.route('/run_cleanser')
def run_cleanser():
    pass
