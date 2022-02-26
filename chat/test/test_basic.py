from flask import abort, url_for
import os
from application.models import User
from application.app import db

def test_app_is_created(app):
        assert app.name == "application.app"

def test_request_returns_404(client):
        assert client.get("/url_que_nao_existe").status_code == 404

def test_homepage_view(client):
        """
        Test that homepage is accessible without login
        """
        assert client.get(url_for('main.index')).status_code == 200 
       
def test_login_view(client):
        """
        Test that login page is accessible without login
        """
        assert client.get(url_for('auth.login')).status_code == 200

def test_signup_view(client):
        """
        Test that login page is accessible without login
        """
        assert client.get(url_for('auth.signup')).status_code == 200 

def login(client, username, password):
    return client.post(url_for('auth.login'), data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    assert client.get(url_for('auth.logout'), follow_redirects=True)

def user():
        db.create_all()
        new_user = User(email=teste@gmail.com, name=Teste, password=generate_password_hash(teste12345, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        assert User.query.filter_by(email=teste@gmail.com).first()