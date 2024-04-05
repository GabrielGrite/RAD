from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__,template_folder="views",static_folder="../public")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:290504@localhost/RAD'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'secret'
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['JWT_BLACKLIST_ENABLE'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()

def create_app():
    login_manager.init_app(app)

    from app import routes
    routes.init_app(app)

    return app




