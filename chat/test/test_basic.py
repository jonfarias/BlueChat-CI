from flask import abort, url_for
import os
from sqlalchemy import create_engine
from flask_login import UserMixin


def test_app_is_created(app):
        assert app.name == "application.app"

def test_request_returns_404(client):
        assert client.get("/url_que_nao_existe").status_code == 404

def test_homepage_view(client):
        assert client.get(url_for('main.index')).status_code == 200 
       
def test_login_view(client):
        assert client.get(url_for('auth.login')).status_code == 200

def test_signup_view(client):
        assert client.get(url_for('auth.signup')).status_code == 200 

def login(client, username, password):
    return client.post(url_for('auth.login'), data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    assert client.get(url_for('auth.logout'), follow_redirects=True)


class User(UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

def user():
        engine = create_engine('sqlite://')
        engine.create_all()
        new_user = User(email=teste@gmail.com, name=Teste, password=generate_password_hash(teste12345, method='sha256'))
        engine.session.add(new_user)
        engine.session.commit()
        assert User.query.filter_by(email=teste@gmail.com).first()