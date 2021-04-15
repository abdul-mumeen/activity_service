import os
from flask import Flask, Blueprint
from flask_script import Manager

import werkzeug

# needed to do this because of open issue in Flask-restplus
werkzeug.cached_property = werkzeug.utils.cached_property

from restapi.restplus import api
from restapi.endpoints.health import ns as health_ns

MYNAME = 'activity'
app = Flask(MYNAME)
app.config['SECRET_KEY'] = 'secret!'

manager = Manager(app=app)

blueprint = Blueprint('api', MYNAME, url_prefix='/api')
api.init_app(blueprint)
api.add_namespace(health_ns)
app.register_blueprint(blueprint)

if __name__ == '__main__':
    manager.run()