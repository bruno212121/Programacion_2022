from flask import Blueprint, current_app, render_template, make_response, url_for, redirect, request
import requests
import json
from . import functions

user = Blueprint('user', __name__, url_prefix='/')

@user.route('/usuario_main/usuario_perfil')
def user_perfil():

    jwt = functions.get_jwt()

    if jwt:
        user = request.cookies.get('id')
        user_info = functions.get_user_info(user)
        user_info = json.loads(user_info.text)

        return render_template('User_perfil.html', jwt = jwt, user_info= user_info)
    else:
        return redirect(url_for('main.login'))

@user.route('/usuario_main/usuario_perfil/usuario_modperfil')
def user_modperfil():
    if request.cookies.get('access_token'):
        api_url = f'{current_app.config["API_URL"]}/poems'
        
        data = { "page": 1, "per_page": 10 }

        headers = { "Content-Type": "application/json" }

        response = requests.get(api_url, json=data, headers=headers) 
        
        return render_template('User_modperfil.html')
    else:
        return redirect(url_for('main.login'))



@user.route('/admin_main/admin_perfil')
def admin_perfil():
    return render_template('admin_perfil.html')

@user.route('/admin_main/crear_usuario')
def crear_usuario():
    return render_template('crear_usuario.html')

@user.route('/admin_main/eliminar_usuario')
def eliminar_usuario():
    return render_template('eliminar_usuario.html')