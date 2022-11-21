from flask import Blueprint, render_template, make_response, request, current_app, redirect, url_for
import requests, json
from . import functions 

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def index():

    data = { "page": 1, "per_page": 6 }
    
    if 'page' in request.args:
        data["page"] = request.args.get('page', '')

    api_url = f'{current_app.config["API_URL"]}/poems' 

    headers = { "Content-Type": "application/json" }
    response = requests.get(api_url, json=data, headers=headers)
    poems = json.loads(response.text)
    print(poems)

    pagination = {}
    pagination["pages"] = json.loads(response.text)["pages"]
    pagination["current_page"] = json.loads(response.text)["page"]

    return render_template('main.html', poems=poems["poems"], pagination=pagination)

@main.route('/usuario_main')
def user_main():
    jwt = request.cookies.get('access_token')
    if jwt:
        data = { "page": 1, "per_page": 6 }
        
        if 'page' in request.args:
            data["page"] = request.args.get('page', '')

        api_url = f'{current_app.config["API_URL"]}/poems'

        headers = { "Content-Type": "application/json" }
        response = requests.get(api_url, json=data, headers=headers) 
        poems = json.loads(response.text)

        pagination = {}
        pagination["pages"] = json.loads(response.text)["pages"]
        pagination["current_page"] = json.loads(response.text)["page"]

        return render_template('User_main.html', poems=poems["poems"], pagination=pagination)
    else:
        return redirect(url_for('main.login'))

@main.route('/admin_main')
def admin_main():
    return render_template('admin_main.html')    


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        jwt = functions.get_jwt()
        api_url = f'{current_app.config["API_URL"]}/user/request.cookies.get("id")'
        headers = functions.get_headers()
    if (request.method == 'POST'): 
        #obtener datos del formulario - Esto lo traigo del HTML con los name de los inputs. 
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        if email != None and password != None: 
            response = functions.login(email, password)
            
            print("login", response)
            if (response.ok): 

                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])

                #Guardar el token en las cookies y devuelve la pagina 
                response = make_response(redirect(url_for('main.user_main')))
                #response = make_response(user_main(jwt=token)) 
                response.set_cookie("access_token", token)
                response.set_cookie("id", user_id)

                return response 
        return(render_template('login.html', error = "Usuario o contraseña incorrectos"))
    else:
        return render_template('login.html')


@main.route("/logout")
def logout():
    resp = make_response(redirect(url_for("main.index")))
    resp.delete_cookie("access_token")
    resp.delete_cookie("id")
    return resp

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = 'poet'
        if name != "" and email != "" and password != "":
            api_url = f'{current_app.config["API_URL"]}auth/register'
            print(api_url)
            data = {"name": name, "email": email, "password": password, "rol": role}
            headers = { "Content-Type": "application/json" }
            response = requests.post(api_url, json = data, headers = headers)
            if response.ok:
                return redirect(url_for("main.login"))
            else:
                return render_template("crear_usuario.html")
        else:
            return render_template("crear_usuario.html")
    else:
        return render_template("crear_usuario.html")