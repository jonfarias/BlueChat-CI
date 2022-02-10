from flask import abort, url_for
import os

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
    return client.get(url_for('auth.logout'), follow_redirects=True)

