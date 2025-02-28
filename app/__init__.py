from flask import Flask
from app.config import Config
from flask_migrate import Migrate
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Inicializar Flask-Migrate
    migrate = Migrate(app, db)


    from app.routes import main
    app.register_blueprint(main)

    return app
