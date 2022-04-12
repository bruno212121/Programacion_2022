import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
import main.resources as resources
#inicializar SQLAlchemy
db = SQLAlchemy()
api = Api()

#Método que inicializará todos los módulos y devolverá la aplicación
def create_app():
    #Inicializar Flask
    app = Flask(__name__)
    #Cargar variables de entorno
    load_dotenv()

    # Si no existe el archivo de base de datos crearlo (solo válido si se utiliza SQLite)

    if not os.path.exists(os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Url de configuración de base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME')
    db.init_app(app)

    #
    #Aquí se inicializarán el resto de los módulos de la aplicación
    #
    api.add_resource(resources.PoemsResource, '/poems')
    api.add_resource(resources.PoemResource, '/poem/<id>')
    api.add_resource(resources.QualificationsResource, '/qualifications')
    api.add_resource(resources.QualificationResource, '/qualification/<id>')
    api.add_resource(resources.UsersResource, '/users')
    api.add_resource(resources.UserResource, '/user/<id>')
    api.init_app(app)
    #Retornar aplicación inicializada
    return app
