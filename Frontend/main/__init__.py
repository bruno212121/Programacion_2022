import os
from flask import Flask
from dotenv import load_dotenv
#from flask_login import LoginManager, login_required



#login_manager = LoginManager()

def create_app():
    #inicia Flask
    app = Flask(__name__, static_url_path='/static') 

    #carga variables de entorno
    load_dotenv()

    app.config['API_URL'] = os.getenv('API_URL')
    #login_manager.init_app(app)

    
    from main.routes import user, poem, main
    app.register_blueprint(main.main)
    app.register_blueprint(user.user)
    app.register_blueprint(poem.poem)

    return app