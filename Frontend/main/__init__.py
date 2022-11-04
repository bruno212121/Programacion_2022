import os
from flask import Flask
from dotenv import load_dotenv
from main.routes import routes



def create_app():
    #inicia Flask
    app = Flask(__name__)
    #carga variables de entorno
    load_dotenv()
    app.register_blueprint(routes.app)
    app.config['API_URL'] = os.getenv('API_URL')
    return app