import os
from flask import Flask
from major import db

def create_app():
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    app.config.from_pyfile('config.py')

    from . import db,auth,site
    db.init_app(app)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(site.bp)
    app.add_url_rule('/',endpoint='index')
    return app
