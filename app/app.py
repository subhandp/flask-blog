# the Flash app

from flask import Flask, g, request, session
from flask_restless import APIManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from config import Configuration # import our configuration data

app = Flask(__name__)
app.config.from_object(Configuration) # use value from our Config
db = SQLAlchemy(app)

api = APIManager(app, flask_sqlalchemy_db=db)
migrate = Migrate(app,db)

bcrypt = Bcrypt(app)

# We will also create a script manager for our app. The script manager allows us to execute special commands within the
# context of our app, directly from the command-line. We will be using the script
# manager to execute the migrate command


manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)
login_manager.login_view = "login"

# handler
@app.before_request
def _before_request():
	g.user = current_user

@app.before_request
def _last_page_visited():
	if "current_page" in session:
		session["last_page"] = session["current_page"]
	session["current_page"] = request.path

