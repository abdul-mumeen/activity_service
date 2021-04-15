"""
Activiy API /health endpoint.
"""
import logging

from flask_restplus import Resource, fields
from ..restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('healthz', description='Health monitoring')

health_status = api.model(
    'Health Status', {
        'status':
        fields.String(
            required=True, readOnly=True, description='Health status')
    })


@ns.route('')
class Health(Resource):
    @ns.marshal_with(health_status)
    def get(self):
        """Return service health status."""
        return {'status': 'healthy'}, 200