from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.model_user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/success')
    else:
        return render_template('index.html')

@app.route('/user/create', methods = ['post'])
def user_create():
    if not User.validate_registration(request.form):
        return redirect ('/') 
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect('/success')

@app.route('/login', methods = ['post'])
def login():
    data = {'email': request.form['email']}
    user = User.get_one_by_email(data)
    if not user:
        flash ("Invalid credentials", 'err_users_login')
        return redirect ('/')
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash ("Invalid credentials", 'err_users_login')
        return redirect ('/')
    session['user_id'] = user.id
    return redirect('/success')


@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect("/")
    return render_template('success.html')

@app.route('/logout')
def logout():
    del session['user_id']
    return redirect('/')

