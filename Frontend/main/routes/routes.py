from flask import Blueprint, render_template

app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/user_main')
def user_main():
    return render_template('User_main.html')

@app.route('/admin_main')
def admin_main():
    return render_template('admin_main.html')
    