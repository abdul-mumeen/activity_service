"""
Event API /events endpoint.
"""
import logging
from datetime import datetime
from flask import request
from flask_restplus import Resource, fields, abort
from ..restplus import api
from services.events import save_event, get_events

log = logging.getLogger(__name__)

ns = api.namespace('events',
                   description='Adding, retrieving and deleting events')

event_post_request_model = api.model(
    'EventCreationModel', {
        'component':
        fields.String(required=True,
                      description='The component the event belongs to.'),
        'data':
        fields.Raw(required=True, description='Json data about the event'),
        'email':
        fields.String(required=True,
                      description='Email address associated with the event'),
        'environment':
        fields.String(required=True,
                      description='The environment the event happened'),
        'message':
        fields.String(required=True,
                      description='Message associated with the event'),
    })

event_response_model = api.clone(
    'EventModel', event_post_request_model, {
        'id':
        fields.String(required=True,
                      description='Unique string indentifying the event.'),
        'created_at':
        fields.String(description='Date the event was generated.'),
    })

events_response_model = api.model(
    'EventsResponseModel', {
        'events':
        fields.List(
            fields.Nested(event_response_model,
                          description='historical events'))
    })


def event_to_resource(event):
    return {
        'id': event.id,
        'component': event.component,
        'created_at': datetime.timestamp(event.created_at),
        'data': event.data,
        'email': event.email,
        'environment': event.environment,
        'message': event.message,
    }


def events_to_resources(events):
    return [event_to_resource(event) for event in events]


@ns.route('/')
class EventsResource(Resource):
    @ns.marshal_with(events_response_model)
    def get(self):
        """Get multiple events resource"""
        log.info(f'GET /events')

        events = []
        try:
            events = get_events()
        except Exception as e:
            log.exception(e)
            abort(400, f'Unable to retrieve events ${e}')

        return {'events': events_to_resources(events)}, 200

    @ns.expect(event_post_request_model, validate=True)
    @ns.marshal_with(event_response_model)
    def post(self):
        """Create an event"""
        log.info(f'POST /events')
        request_payload = request.get_json()
        try:
            event = save_event(request_payload)
        except Exception as e:
            log.exception(e)
            abort(500, e)

        return event_to_resource(event), 201