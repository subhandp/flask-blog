# datetime - current date and time
# re - string manipulation (regular expressionW)
import datetime, re
from app import db
from app import login_manager
from app import bcrypt

# app _before.request()
@login_manager.user_loader
def _user_loader(user_id):
    return User.query.get(int(user_id))

# The slugify function takes a string such as A post about Flask and uses a regular
# expression to turn a string that is human-readable in to a URL, and
# ipython
# from models import *
# var = Entry(title='',body='')
# db.session.add(var)
# db.session.commit()
# var.id
# var = Entry.query.all()
# Entry.query.order_by(Entry.title.asc()).all() / .first()
# Entry.query.filter(Entry.title == 'First entry').all()


# so returns a-post-about-flask.
def slugify(s):
    return re.sub('[^\w]+', '-', s).lower()

# By creating the entry_tags table, we have established
# a link between the Entry and Tag models
entry_tags = db.Table('entry_tags',
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                      db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'))
                      )

# extends db.Model
class Entry(db.Model):
    STATUS_PUBLIC = 0
    STATUS_DRAFT = 1
    STATUS_DELETED = 2

    id = db.Column(db.Integer, primary_key=True) # primary auto increment
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True) # The URL-friendly representation of the title
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    created_timestamp = db.Column(db.DateTime, default = datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )

    # This function creates a new property on the Entry model
    # that allows us to easily read and write the tags for a
    # given blog entry.

    # We are setting the tags attribute of the Entry class equal to the return value of the
    # db.relationship function. The first two arguments, 'Tag' and secondary=entry_
    # tags , instruct SQLAlchemy that we are going to be querying the Tag model via
    # the entry_tags table. The third argument creates a back-reference, allowing us
    # to go from the Tag model back to the associated list of blog entries. By specifying
    # lazy='dynamic', we instruct SQLAlchemy that, instead of it loading all the
    # associated entries for us, we want a Query object instead
    tags = db.relationship('Tag', secondary=entry_tags,
                           backref=db.backref('entries', lazy='dynamic'))

    # backref untuk mencari hubungan antara Tag model dgn Entry Model
    # tags atribut mencari hubungan antara Entry model dgn Tag model

    # We've overridden the constructor for the class ( __init__ ) so that, when a new model
    # is created, it automatically sets the slug for us based on the title.
    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs) # call parent constructor
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)

    # The last piece is the __repr__ method that is used to generate a helpful
    # representation of instances of our Entry class. The specific meaning of __repr__
    # is not important but allows you to reference the object that the program is working
    # with, when debugging.
    def __repr__(self):
        return '<Entry: %s>' % self.title


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Tag %s>' % self.name


# In IPython, you can use an underscore (_) to reference the return-
# value of the previous line.


class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(255))
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)
    active = db.Column(db.Boolean, default=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)


    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    @staticmethod
    def make_password(plaintext):
        return bcrypt.generate_password_hash(plaintext)


    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash, raw_password)


    @classmethod
    def create(cls, email, password, **kwargs):
        return User(
            email=email,
            password_hash=User.make_password(password),
            **kwargs)


    @staticmethod
    def authenticate(email, password):
        user = User.query.filter(User.email == email).first()
        if user and user.check_password(password):
            return user
        return False