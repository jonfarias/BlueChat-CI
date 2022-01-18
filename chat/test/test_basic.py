from flask import abort, url_for
import os

def test_app_is_created(app):
        assert app.name == "chat.app"

def test_request_returns_404(client):
        assert client.get("/url_que_nao_existe").status_code == 404

#def test_500_internal_server_error(client):
        # create route to abort the request with the 500 Error
#        @client.route('/500')
#        def internal_server_error():
#            abort(500)

#        assert client.get("/500").status_code == 500

        #response = self.client.get('/500')
        #self.assertEqual(response.status_code, 500)
        #self.assertTrue("500 Error" in response.data)

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

#def test_login_logout(client):
    """Make sure login and logout works."""

#    username = os.environ.get("USERNAME")
#    password = os.environ.get("PASSWORD")

#    rv = login(client, username, password)
#    assert b'You were logged in' in rv.data

#    rv = logout(client)
#    assert b'You were logged out' in rv.data

#    rv = login(client, f"{username}x", password)
#    assert b'Invalid username' in rv.data

#    rv = login(client, username, f'{password}x')
#    assert b'Invalid password' in rv.data

#def test_logout_view(client):

#        target_url = url_for('auth.logout')
#        redirect_url = url_for('auth.login', next=target_url)
#        response = client.get(target_url)
#        assert client.get(response).status_code == 302
        #assert client.assertRedirects(response, redirect_url)



#def test_chat_view(self):

#        target_url = url_for('main.chat')
#        redirect_url = url_for('auth.login', next=target_url)
#        response = self.client.get(target_url)
#        self.assertEqual(response.status_code, 302)
#        self.assertRedirects(response, redirect_url)

#def test_profile_view(self):

#        target_url = url_for('main.profile')
#        redirect_url = url_for('auth.login', next=target_url)
#        response = self.client.get(target_url)
#        self.assertEqual(response.status_code, 302)
#        self.assertRedirects(response, redirect_url)
