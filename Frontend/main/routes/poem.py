from flask import Blueprint, render_template, url_for, redirect, json, current_app, request
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


"""
cookie = request.cookies.get('access_token')
    if cookie:
        user_id = request.cookies.get('id')

        url = 'http://127.0.0.1:8500/user' + f'/{user_id}'

        headers = {'Content-type': 'application/json', 'Authorization': f'Bearer {cookie}'}

        response = requests.get(url, headers=headers)

        user = json.loads(response.text)

        print(user)

        return render_template('profile.html', user=user)
    return render_template('profile.html'
"""

@poem.route('/usuario_main/crear_poema', methods=['GET','POST'])
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
                    return redirect(url_for('main.user_main'))
                else:
                    return redirect(url_for('poem.crear_poema'))
            else:
                return redirect(url_for('poem.crear_poema'))
        else:
            return render_template('Crear_poema.html', jwt=jwt) 
    else:
        return redirect(url_for('main.login'))