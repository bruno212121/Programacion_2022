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
        print("user", user)
        user_info = functions.get_user_info(user)
        user_info = json.loads(user_info.text)
        print("user infoo",user_info)

        return render_template('User_perfil.html', jwt = jwt, user_info= user_info)
    else:
        return redirect(url_for('main.login'))

@user.route('/usuario/modperfil', methods=['GET', 'POST'])
def user_modperfil():
    jwt = request.cookies.get('access_token')
    if jwt:
        user_id = request.cookies.get('id')
        if request.method == 'GET':
            api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
            headers = {'Content-type': 'application/json', 'Authorization': f"Bearer {jwt}"}
            response = requests.get(api_url, headers=headers)
            user = json.loads(response.text)
            return render_template('User_modperfil.html', user=user)
            
        if request.method == 'POST':
            name = request.form['Name']
            print("name", name)
            password = request.form['Password']
            print("password", password)
            api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
            data = {"name": name, "plain_password": password}
            headers = {'Content-type': 'application/json', 'Authorization' : f"Bearer {jwt}"}
            if name != "" and password != "":
                response = requests.put(api_url, json=data, headers=headers)
                if response.status_code == 200:
                    response = json.loads(response.text)
                    return redirect(url_for('user.user_perfil'))
                else:
                    return redirect(url_for('user.user_perfil'))
            elif name != "":
                data = {"name": name}
                response = requests.put(api_url, json=data, headers=headers)
                if response.status_code == 200:
                    response = json.loads(response.text)
                    return redirect(url_for('user.user_perfil'))
                else:
                    return redirect(url_for('user.user_perfil'))
            elif password != "":
                data = {"plain_password": password}
                response = requests.put(api_url, json=data, headers=headers)
                if response.status_code == 200:
                    response = json.loads(response.text)
                    return redirect(url_for('user.user_perfil'))
                else:
                    return redirect(url_for('user.user_perfil'))
            else:
                return redirect(url_for('user.user_modperfil'))
    return redirect(url_for('main.login'))

@user.route('/eliminar_usuario', methods=['GET', 'POST'])
def eliminar_usuario():
    jwt = request.cookies.get('access_token')
    if jwt:
        api_url = f'{current_app.config["API_URL"]}/user/{request.cookies.get("id")}'
        headers = {"Content-Type" : "application/json","Authorization":f"Bearer {jwt}"}
        response = requests.delete(api_url, headers=headers)
        return redirect(url_for('main.logout'))
    else:
        return redirect(url_for('main.login'))



@user.route('/admin_main/admin_perfil')
def admin_perfil():
    return render_template('admin_perfil.html')

@user.route('/admin_main/crear_usuario')
def crear_usuario():
    return render_template('crear_usuario.html')

