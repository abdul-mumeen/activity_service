"""
Event API /events endpoint.
"""
import logging
import string
import json
from flask import request, json
from flask_restplus import Resource, fields, abort
from ..restplus import api
from models.event import Event

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


@ns.route('/')
class EventsResource(Resource):
    @ns.marshal_with(events_response_model)
    def get(self):
        """Get multiple events resource"""
        log.info(f'GET /events')

        events = []
        try:
            events = Event.get_events()
        except Exception as e:
            log.exception(e)
            abort(400, f'Unable to retrieve events ${e}')

        events_data_list = [event.to_dict() for event in events]

        return {'events': events_data_list}, 200

    @ns.expect(event_post_request_model, validate=True)
    @ns.marshal_with(event_response_model)
    def post(self):
        request_payload = request.get_json()

        component = request_payload.get('component')
        data = request_payload.get('data')
        email = request_payload.get('email')
        environment = request_payload.get('environment')
        message = request_payload.get('message')

        request_data = {
            'component': component,
            'data': data,
            'email': email,
            'environment': environment,
            'message': message
        }

        try:
            event = Event(request_data)
            event.save()
        except Exception as e:
            log.exception(e)
            abort(500, e)

        return event.to_dict(), 201