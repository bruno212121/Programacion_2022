import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

#inicializar SQLAlchemy
db = SQLAlchemy()
api = Api()
jwt = JWTManager()

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

    import main.resources as resources
    #
    #Aquí se inicializarán el resto de los módulos de la aplicación
    #
    api.add_resource(resources.PoemsResource, '/poems')
    api.add_resource(resources.PoemResource, '/poem/<id>')
    api.add_resource(resources.ScoreResource, '/score/<id>')
    api.add_resource(resources.ScoresResource, '/scores')
    api.add_resource(resources.UsersResource, '/users')
    api.add_resource(resources.UserResource, '/user/<id>')

    api.init_app(app)

    # Cargar clave secreta
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    # Cargar tiempo de expiración de los tokens
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)

    from main.auth import routes
    # Importar blueprint
    app.register_blueprint(routes.auth)

    #Retornar aplicación inicializada
    return app
