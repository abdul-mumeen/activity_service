import json
import re
from datetime import datetime
from db import db
from models.event import Event
from flask_restplus import abort


def validate_event_request_data(component, data, email, environment, message):
    if (not re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                      email)):
        raise Exception('Invalid email address.')

    if not (component and component.trim()):
        raise Exception('Component can not be empty.')
    if not (environment and environment.trim()):
        raise Exception('Environment can not be empty.')
    if not (message and message.trim()):
        raise Exception('Message can not be empty.')
    try:
        json.dumps(data)
    except:
        raise Exception('Data is not a valid JSON object.')


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


def get_events(params):
    component = params.get('component')
    from_date = params.get('from_date')
    email = params.get('email')
    environment = params.get('environment')
    message = params.get('message')

    query = Event.query
    if component:
        query = query.filter_by(component=component)
    if email:
        query = query.filter_by(email=email)
    if environment:
        query = query.filter_by(environment=environment)
    if message:
        query = query.filter(Event.message.like(f'%{message}%'))
    if from_date:
        try:
            from_date_object = datetime.strptime(from_date, '%m-%d-%Y')
            query = query.filter(Event.created_at >= from_date_object)
        except Exception as e:
            abort(400, 'Invalid date specified.')
    return query.all()


def save_changes(event):
    db.session.add(event)
    db.session.commit()