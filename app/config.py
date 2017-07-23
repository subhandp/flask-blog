# configuration variables for our Flask app

import os 

class Configuration(object):
	APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
	DEBUG = True
	SECRET_KEY = 'this is sparta!'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/blog.db' % APPLICATION_DIR
	STATIC_DIR = os.path.join(APPLICATION_DIR, 'static')
	IMAGES_DIR = os.path.join(STATIC_DIR, 'images')