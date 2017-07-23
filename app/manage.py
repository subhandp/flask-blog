from app import manager
from main import *

# This looks very similar to main.py ,
# the key difference being, instead of calling app.
# run(), we are calling manager.run()
if __name__ == '__main__':
	manager.run()