"""
flask-restplus specific initializations.
"""
import logging

from flask_restplus import Api

log = logging.getLogger(__name__)

api = Api(version='1',
          title='Activity service',
          description='Service for saving and retrieving historical events.')


@api.errorhandler
def default_error_handler(err):
    message = 'An unhandled exception occurred: {}'.format(err)
    # Flask fully logs this exception, so we don't have to
    # log.exception(message)

    return {'message': message}, 500