from flask import request, current_app 
import requests, json

def login(email, password):
    #es la url que utilizamos en insomnia
    api_url = f'{current_app.config["API_URL"]}/auth/login'
    #Envio de token
    data = { "email": email, "password": password }
    headers = { "Content-Type": "application/json" }

    return requests.post(api_url, json=data, headers=headers)

def get_jwt():
    return request.cookies.get('access_token')


def get_poems_by_id(id, page = 1, perpage = 3):

    api_url = f'{current_app.config["API_URL"]}/poems' 
    # Envio de la pagina y cuantos datos por pagina.
    data = {"page": page, "perpage": perpage, "userId": id}
    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    headers = get_headers(without_token = True)
    # Creamos el response y le enviamos el data y headers.
    return requests.get(api_url, json = data, headers = headers)

#Obtengo el email del usuario
def get_headers(without_token = False, jwt = None):
    if jwt == None and without_token == False:
        return {"Content-Type" : "application/json", "Authorization" : f"Bearer {get_jwt()}"}
    if jwt and without_token == False:
        return {"Content-Type" : "application/json", "Authorization" : f"Bearer {jwt}"}
    else:
        return {"Content-Type" : "application/json"}

