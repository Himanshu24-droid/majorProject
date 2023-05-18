import os
from flask import Flask
from major import db
from dotenv import load_dotenv
import secrets

def create_app():
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=secrets.token_hex(16)
    )
    app.config.from_pyfile('config.py')
    load_dotenv()
    from . import db,auth,site
    db.init_app(app)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(site.bp)
    app.add_url_rule('/',endpoint='index')
    
    return app
