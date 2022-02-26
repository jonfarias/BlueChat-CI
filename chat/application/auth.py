from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from flask_socketio import join_room, leave_room, emit
from .app import socketio
from .app import db

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

    if not user or not check_password_hash(user.password, password): 
        flash('Ops algo deu errado, email ou senha errados.')
        return redirect(url_for('auth.login')) 

    login_user(user, remember=remember)
    flash('Login feito com sucesso.')
    return redirect(url_for('main.chat'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() 

    if user: 
        flash('O email inserido já existe')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # Adiciona um novo usuário ao banco de dados
    db.session.add(new_user)
    db.session.commit()

    flash('Usuário Cadastrado com Sucesso')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    session.pop('email', None)
    session.pop('password', None)
    logout_user()
    return redirect(url_for('main.index'))

#Socketio
@socketio.on('join', namespace='/chat')
def join(message):
    room = 'room'
    join_room(room)
    mensage_join = session.get('email') + " " + 'entrou'
    emit('status', {'msg':  mensage_join}, room=room)
    
#Enviar e Receber Mensagens
@socketio.on('text', namespace='/chat')
def text(message):
    room = 'room'
    mensage_text = session.get('email') + " : " + message['msg']
    emit('message', {'msg': mensage_text}, room=room)

#Sair do chat
#@socketio.on('left', namespace='/chat')
#def left(message):
    #room = session.get('room')
#    room = 'room'
#    username = session.get('username')
#    leave_room(room)
#    session.clear()
#    emit('status', {'msg': username + ' saiu'}, room=room)