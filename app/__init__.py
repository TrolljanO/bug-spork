from flask import Flask
from app.routes import main


def create_app():
    app = Flask(__name__)

    # Configurações do app
    app.config.from_object('app.config.Config')

    # Registrar rotas
    app.register_blueprint(main)

    return app
