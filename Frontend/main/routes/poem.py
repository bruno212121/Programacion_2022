from flask import Blueprint, render_template, url_for, redirect, json, current_app, request
from flask import json
import requests
from . import functions

poem = Blueprint('poem', __name__, url_prefix='/')

poems = [{"id":0 , 'title': 'Poem 1', 'body': 'This is the body of poem 1'}] 


@poem.route('/usuario_main/mis_poemas')
def mis_poema():
    jwt = functions.get_jwt()
    if jwt:

        user_id = request.cookies.get('id')
        print("user_id", user_id)

        resp = functions.get_poems_by_id(user_id)
        print("api_url", resp)
        
        poems = json.loads(resp.text)
        print("poems", poem)
        poemsList = poems["poems"]

        return render_template('mispoemas.html', jwt=jwt, poems=poemsList)
    else:
        return redirect(url_for('main.login'))


@poem.route('/crear_poema', methods=['GET','POST'])
def crear_poema():
    jwt = functions.get_jwt()
    if jwt:
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            print(title)
            print(body)
            id = request.cookies.get("id")
            data = {"title":title,"body":body,"userId": id}
            headers = { "Content-Type": "application/json", "Authorization": f"Bearer {jwt}"}
            if title != "" and body != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poems', json=data, headers=headers)
                print(response)
                if response.ok: 
                    response = json.loads(response.text) 
                    print(response)
                    return redirect(url_for('main.user_main'))
                else:
                    return redirect(url_for('poem.crear_poema'))
            else:
                return redirect(url_for('poem.crear_poema'))
        else:
            return render_template('Crear_poema.html', jwt=jwt) 
    else:
        return redirect(url_for('main.login'))

@poem.route('/poem/<id>', methods=['GET'])
def poema(id):
    jwt = functions.get_jwt()
    api_url = f'{current_app.config["API_URL"]}/poem/{id}'
    headers = {f"Content-Type" : "application/json", "Authorization" : "Bearer {}".format(jwt)}
    response = requests.get(api_url, headers=headers)
    poems = json.loads(response.text)
    return render_template('ver_poema.html', poems = poems)

@poem.route('/poem/<id>/edit', methods=['GET','POST'])
def edit_poem(id):
    jwt = functions.get_jwt()
    if jwt:
        if request.method == 'GET':
                api_url = f'{current_app.config["API_URL"]}/poem/{id}'
                headers = { "Content-Type": "application/json", "Authorization": f"Bearer {jwt}"}
                response = requests.get(api_url, headers=headers)
                poem = json.loads(response.text)
                return render_template('editar_poema.html', poem = poem)
        else:
            if request.method == 'POST':
                title = request.form['title']
                body = request.form['body']
                print(title)
                print(body)
                data = {"title":title,"body":body}
                headers = { "Content-Type": "application/json", "Authorization": f"Bearer {jwt}"}
                api_url = f'{current_app.config["API_URL"]}/poem/{id}'
                response = requests.put(api_url, json=data, headers=headers)
                return redirect(url_for('main.user_main', id=id))
    return redirect(url_for('main.login'))      

@poem.route('/poem/<id>/delete', methods=['GET'])
def delete_poem(id):
    jwt = functions.get_jwt()
    if jwt:
        api_url = f'{current_app.config["API_URL"]}/poem/{id}'
        headers = { "Content-Type": "application/json", "Authorization": f"Bearer {jwt}"}
        response = requests.delete(api_url, headers=headers)
        return redirect(url_for('main.user_main'))
    else:
        return redirect(url_for('main.login'))