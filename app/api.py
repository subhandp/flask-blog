from flask_restless import ProcessingException

from app import api
from models import Comment
from entries.forms import CommentForm

# The code in api.py calls the create_api() method on our APIManager object.
# This method will populate our app with additional URL routes and view code that,
# together, constitute a RESTful API. The methods parameter indicates that we will
# allow only GET and POST requests (meaning comments can be read or created, but
# not edited or deleted).
# api.create_api(Comment, methods=['GET', 'POST'])

# raise -> throw error

# Unfortunately for us, our API is not performing any type of validation on the
# incoming data. In order to validate the POST data, we need to use a hook provided
# by Flask-Restless. Flask-Restless calls these hooks request preprocessors and
# postprocessors.
# Let's take a look at how to use the POST preprocessor to perform some validation on
# our comment data


def post_preprocessor(data, **kwargs):
    form = CommentForm(data=data)
    if form.validate():
        return form.data
    else:
        raise ProcessingException(
            description='Invalid form submission.',
            code=400
        )

api.create_api(
    Comment,
    methods=['GET', 'POST'],
    preprocessors={
        'POST': [post_preprocessor]
    }
)

# Our API will now validate the submitted comment using the validation logic from
# our CommentForm . We do this by specifying a preprocessor for the POST method.
# The POST preprocessor, which we've implemented as post_preprocessor , accepts
# the deserialized POST data as an argument. We can then feed that data into our
# CommentForm and call it's validate() method. In the event where validation fails,
# we will raise a ProcessingException , signaling to Flask-Restless that this data was
# unprocessable and returning a 400 Bad Request response.