import json
import re
from db import db
from models.event import Event
from flask_restplus import abort


def validate_event_request_data(component, data, email, environment, message):
    if (not re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                      email)):
        raise Exception('Invalid email address.')

    if (not component):
        raise Exception('Component can not be empty')
    if (not environment):
        raise Exception('Environment can not be empty')
    if (not message):
        raise Exception('Message can not be empty')
    try:
        json.dumps(data)
    except:
        raise Exception('Data is not a valid JSON object')


def save_event(request_payload):
    component = request_payload.get('component')
    data = request_payload.get('data')
    email = request_payload.get('email')
    environment = request_payload.get('environment')
    message = request_payload.get('message')

    try:
        validate_event_request_data(component, data, email, environment,
                                    message)
    except Exception as e:
        abort(400, e)

    request_data = {
        'component': component,
        'data': data,
        'email': email,
        'environment': environment,
        'message': message
    }

    event = Event(request_data)
    save_changes(event)
    return event


def get_events():
    return Event.query.all()


def save_changes(event):
    db.session.add(event)
    db.session.commit()