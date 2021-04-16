from datetime import date
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db


class Event(db.Model):
    """
    Event Model
    """

    # table name
    __tablename__ = 'events'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    component = db.Column(db.String())
    created_at = db.Column(db.DateTime)
    data = db.Column(db.JSON)
    email = db.Column(db.String())
    environment = db.Column(db.String())
    message = db.Column(db.String())

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.component = data.get('component')
        self.created_at = date.utcnow()
        self.data = data.get('data')
        self.email = data.get('email')
        self.environment = data.get('environment')
        self.message = data.get('message')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_events():
        return Event.query.all()

    @staticmethod
    def get_event(id):
        return Event.query.get(id)

    def __repr(self):
        return '<id {}>'.format(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'component': self.component,
            'created_at': self.created_at,
            'data': self.data,
            'email': self.email,
            'environment': self.environment,
            'message': self.message,
        }