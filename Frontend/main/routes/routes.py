from flask import Blueprint, render_template, make_response, url_for, redirect, request
import requests
import json

app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    if request.cookies.get('access_token'):
        return render_template('main.html')
    else:
        return redirect(url_for('app.login'))

@app.route('/usuario_main')
def user_main():
    return render_template('User_main.html')

@app.route('/usuario_main/crear_poema')
def crear_poema():
    return render_template('Crear_poema.html')

@app.route('/usuario_main/mis_poemas')
def mis_poema():
    return render_template('mispoemas.html')

@app.route('/usuario_main/usuario_perfil')
def user_perfil():
    return render_template('User_perfil.html')

@app.route('/usuario_main/usuario_perfil/usuario_modperfil')
def user_modperfil():
    return render_template('User_modperfil.html')
    
@app.route('/admin_main')
def admin_main():
    return render_template('admin_main.html')

@app.route('/admin_main/admin_perfil')
def admin_perfil():
    return render_template('admin_perfil.html')

@app.route('/admin_main/crear_usuario')
def crear_usuario():
    return render_template('crear_usuario.html')

@app.route('/admin_main/eliminar_usuario')
def eliminar_usuario():
    return render_template('eliminar_usuario.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email)
        print(password)

        #es la url que utilizamos en insomnia
        api_url = "http://127.0.0.1:5000/auth/login"
        
        #Envio de token
        data = {"email" : email, "password" : password}
        
        headers = {"Content-Type" : "application/json"}
        
        response = requests.post(api_url, json = data, headers = headers) 
        if response.status_code == 200:
            print(response.text)
            print(response.status_code)
            
            #obtener el token desde response
            token = json.loads(response.text)
            token = token["access_token"]
            print(token) 

            #Guardar el token en las cookies y devuelve la pagina 
            response = make_response(redirect("main.index"))
            response.set_cookie("access_token", token)

            return response 
            #return render_template('login.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')
