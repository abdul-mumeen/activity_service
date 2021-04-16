import os
from flask import Flask, Blueprint
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import werkzeug

# needed to do this because of open issue in Flask-restplus
werkzeug.cached_property = werkzeug.utils.cached_property

from restapi.restplus import api
from restapi.endpoints.health import ns as health_ns
from restapi.endpoints.events import ns as events_ns

from db import db
from models.event import Event

MYNAME = 'activity'
app = Flask(MYNAME)
app.config['SECRET_KEY'] = 'secret!'

# db setup
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
db_name = os.environ['POSTGRES_DB']
host = os.environ['POSTGRES_HOST']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:5432/{db_name}'  # 'postgres://abdulmumeen@localhost:5432/activity_app_db'
db.init_app(app)
migrate = Migrate(app=app, db=db, event=Event)

manager = Manager(app=app)

# db command line manager
manager.add_command('db', MigrateCommand)

blueprint = Blueprint('api', MYNAME, url_prefix='/api')
api.init_app(blueprint)
api.add_namespace(health_ns)
api.add_namespace(events_ns)
app.register_blueprint(blueprint)

if __name__ == '__main__':
    manager.run()