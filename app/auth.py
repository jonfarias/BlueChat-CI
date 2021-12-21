from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from flask_socketio import join_room, leave_room, emit
from . import socketio
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    session['email'] = email
    session['password'] = password

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Ops algo deu errado, email ou senha errados.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    #flash('Login feito com sucesso.')
    return redirect(url_for('main.chat'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('O email inserido já existe')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

#Socketio
@socketio.on('join', namespace='/chat')
def join(message):
    room = 'room'
    join_room(room)
    emit('status', {'msg':  session.get('email') + ' entrou'}, room=room)
    
#Enviar e Receber Mensagens
@socketio.on('text', namespace='/chat')
def text(message):
    room = 'room'
    emit('message', {'msg': session.get('email') + ' : ' + message['msg']}, room=room)

#Sair do chat
#@socketio.on('left', namespace='/chat')
#def left(message):
    #room = session.get('room')
#    room = 'room'
#    username = session.get('username')
#    leave_room(room)
#    session.clear()
#    emit('status', {'msg': username + ' saiu'}, room=room)