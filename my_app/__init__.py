from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load environmet variables
load_dotenv('./env')

# Create app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")



#_______________________________________________________________________________
# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)
if db:
    print('DB IS READY!!!\n')

#_______________________________________________________________________________
# Others
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

from my_app import routes
