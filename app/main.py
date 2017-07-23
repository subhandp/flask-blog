# Entry-point for executing our application

from app import app, db # import our Flask app
import models
import views

# In order to access these new views, we need to register our blueprint with our main
# Flask app object 

# We will also instruct our app that we want our entries' URLs to live at the prefix /entries .

from entries.blueprint import entries
app.register_blueprint(entries, url_prefix='/entries')

if __name__ == '__main__':
	app.run()

	