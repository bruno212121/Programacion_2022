from flask import Blueprint, current_app, render_template, make_response, url_for, redirect, request
import requests
import json

app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    if request.cookies.get('access_token'):

        api_url = f'{current_app.config["API_URL"]}/poems' 

        data = { "page": 1, "per_page": 10 }

        headers = { "Content-Type": "application/json" }

        response = requests.get(api_url, json=data, headers=headers)
        print(response.status_code)  
        print(response.text)

        poems = json.loads(response.text)
        print(poems)

        return render_template('main.html', poems=poems["poems"])
    else:
        return redirect(url_for('app.login'))


@app.route('/usuario_main')
def user_main():
    if request.cookies.get('access_token'):
        
        api_url = f'{current_app.config["API_URL"]}/poems'

        data = { "page": 1, "per_page": 10 }

        headers = { "Content-Type": "application/json" }

        response = requests.get(api_url, json=data, headers=headers) 
        print(response.status_code)  
        print(response.text)
        poems = json.loads(response.text)
        print(poems)
        return render_template('User_main.html', poems=["Poems"])
    else:
        return redirect(url_for('app.login'))

@app.route('/usuario_main/crear_poema', methods=['GET','POST'])
def crear_poema():
    jwt = request.cookies.get('access_token')
    if jwt:
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            id = request.cookies.get('id')
            data = {"title":title,"body":body,"userId": id}
            headers = { "Content-Type": "application/json", "Authorization": f"Bearer {jwt}"}
            if title != "" and body != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poems', json=data, headers=headers)
                if response.ok:
                    response = json.loads(response.text)
                    return redirect(url_for('app.user_main'))
                else:
                    return redirect(url_for('app.crear_poema'))
            else:
                return redirect(url_for('app.crear_poema'))
        else:
            return render_template('Crear_poema.html', jwt=jwt) 
    else:
        return redirect(url_for('app.login'))

@app.route('/usuario_main/mis_poemas')
def mis_poema():
    if request.cookies.get('access_token'):
        
        api_url = f'{current_app.config["API_URL"]}/poems'
        
        data = { "page": 1, "per_page": 10 }

        headers = { "Content-Type": "application/json" }

        response = requests.get(api_url, json=data, headers=headers) 
    
        return render_template('mispoemas.html', poems = ["Poems"])
    else:
        return redirect(url_for('app.login'))

@app.route('/usuario_main/usuario_perfil')
def user_perfil():
    if request.cookies.get('access_token'):
        api_url = f'{current_app.config["API_URL"]}/poems'
        
        data = { "page": 1, "per_page": 10 }

        headers = { "Content-Type": "application/json" }

        response = requests.get(api_url, json=data, headers=headers) 
        
        return render_template('User_perfil.html', poems = ["Poems"])
    else:
        return redirect(url_for('app.login'))

@app.route('/usuario_main/usuario_perfil/usuario_modperfil')
def user_modperfil():
    if request.cookies.get('access_token'):
        api_url = f'{current_app.config["API_URL"]}/poems'
        
        data = { "page": 1, "per_page": 10 }

        headers = { "Content-Type": "application/json" }

        response = requests.get(api_url, json=data, headers=headers) 
        
        return render_template('User_perfil.html', poems = ["Poems"])
    else:
        return redirect(url_for('app.login'))

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
    if (request.method == 'POST'):
        #obtener datos del formulario - Esto lo traigo del HTML con los name de los inputs. 
        email = request.form['email']
        password = request.form['password']
        print(email, password)

        if email != None and password != None: 
            #es la url que utilizamos en insomnia
            api_url = f'{current_app.config["API_URL"]}/auth/login'
            #Envio de token
            data = {"email" : email, "password" : password}
            headers = {"Content-Type" : "application/json"}
            
            response = requests.post(api_url, json = data, headers = headers) 
            print("login", response)
            if response.status_code == 200: 

                print(response.status_code)
                print(response.text)

                #obtener el token desde response
                token = json.loads(response.text)
                token = token["access_token"]
                print(token) 

                #Guardar el token en las cookies y devuelve la pagina 
                response = make_response(redirect(url_for('app.user_main')))
                response.set_cookie("access_token", token)

                return response 
                #return render_template('login.html')
            else:
                return render_template('login.html')
        return(render_template('login.html', error = "Usuario o contraseña incorrectos"))
    else:
        return render_template('login.html')
