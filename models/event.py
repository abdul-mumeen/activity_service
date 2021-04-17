from datetime import date, datetime
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
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
        # self.created_at = datetime.utcnow()
        self.data = data.get('data')
        self.email = data.get('email')
        self.environment = data.get('environment')
        self.message = data.get('message')

    def __repr(self):
        return '<id {}>'.format(self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
