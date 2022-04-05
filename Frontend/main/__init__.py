import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    #inicia Flask
    app = Flask(__name__)
    #carga variables de entorno
    load_dotenv()
    return app