from flask import Blueprint, render_template, make_response, request, current_app, redirect, url_for
import requests, json
from . import functions 

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/')
def index():
    
    api_url = f'{current_app.config["API_URL"]}/poems' 

    data = { "page": 1, "per_page": 15 }

    headers = { "Content-Type": "application/json" }

    response = requests.get(api_url, json=data, headers=headers)
    print(response.status_code)  
    print(response.text)

    poems = json.loads(response.text)
    print(poems)

    return render_template('main.html', poems=poems["poems"])

@main.route('/usuario_main')
def user_main():
    if request.cookies.get('access_token'):
        
        api_url = f'{current_app.config["API_URL"]}/poems'

        data = { "page": 1, "per_page": 15 }

        headers = { "Content-Type": "application/json" }

        response = requests.get(api_url, json=data, headers=headers) 
        print(response.status_code)  
        print(response.text)
        poems = json.loads(response.text)
        print(poems)
        return render_template('User_main.html', poems=poems["poems"])
    else:
        return redirect(url_for('main.login'))

@main.route('/admin_main')
def admin_main():
    return render_template('admin_main.html')    


@main.route('/login', methods=['GET', 'POST'])
def login():
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
    resp = make_response(redirect(url_for("main.login")))
    resp.delete_cookie("access_token")
    resp.delete_cookie("id")
    return resp

