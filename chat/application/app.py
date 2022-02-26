from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from flask_socketio import SocketIO
from flask_session import Session
#Environment Variables
#from dotenv import load_dotenv
import os

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")
#load_dotenv()

def create_app():
    app = Flask(__name__)

    user = os.environ.get("MYSQL_USER")
    pwd = os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT")
    database = os.environ.get("MYSQL_DATABASE")

    url = "mysql+pymysql://%s:%s@%s:%s/%s" %(user, pwd, host, port, database)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    socketio.init_app(app)
    Session(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    return app