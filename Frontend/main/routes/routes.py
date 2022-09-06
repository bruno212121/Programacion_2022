from flask import Blueprint, render_template

app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/usuario_main')
def user_main():
    return render_template('User_main.html')

@app.route('/usuario_main/crear_poema')
def crear_poema():
    return render_template('Crear_poema.html')

@app.route('/usuario_main/mis_poemas')
def mispoema():
    return render_template('mispoemas.html')

@app.route('/usuario_main/usurario_perfil')
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

@app.route('/login')
def login():
    return render_template('login.html')

