# Blueprints provide a nice API for encapsulating a group of related routes and
# templates. In smaller applications, typically everything gets registered on the app
# object (that is, app.route ). When an application has distinct components, as ours
# does, blueprints can be used to separate the various moving parts. Since the /
# entries/ URL is going to be devoted entirely to our blog entries, we will create a
# blueprint and then define views to handle the routes that we described previously.

import os

from flask import Blueprint
from flask import g
from flask import request, flash, render_template, redirect, url_for
from werkzeug import secure_filename
from flask_login import login_required

from helpers import object_list
from models import Entry,Tag
from entries.forms import EntryForm, ImageForm
from app import db, app

entries = Blueprint('entries', __name__,
	template_folder='templates')

def entry_list(template, query, **context):
	query = filter_status_by_user(query)
	valid_statuses = (Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT)
	query = query.filter(Entry.status.in_(valid_statuses))
	if request.args.get('q'):
		search = request.args['q']
		query = query.filter(
			(Entry.body.contains(search)) |
			(Entry.title.contains(search))
			)

	return object_list(template, query, **context)

def get_entry_or_404(slug, author=None):
	query = Entry.query.filter(Entry.slug == slug)
	if author:
		query = query.filter(Entry.author == author)
	else:
		query = filter_status_by_user(query)
	return query.first_or_404()

def filter_status_by_user(query):
	if not g.user.is_authenticated:
		query.filter(Entry.status == Entry.STATUS_PUBLIC)
	else:
		query = query.filter(
				(Entry.status == Entry.STATUS_PUBLIC) |
				((Entry.author == g.user) & (Entry.status != Entry.STATUS_DELETED))
		)
	return query

# We are importing the object_list helper function and passing it the name of a
# template and the query representing the entries we wish to display. As we build out
# the rest of these views, you will see how little helper functions such as object_list
# make Flask development quite easy.


# When a file is uploaded, Flask will
# store it in request.files , which is a special dictionary keyed by the name of the
# form field. We do some path joining using secure_filename to prevent malicious
# filenames and to generate the correct path to the static/images directory, and then
# save the uploaded file to disk
@entries.route('/image-upload/', methods=['GET', 'POST'])
@login_required
def image_upload():
	form = ImageForm()
	if request.method == 'POST':
		form = ImageForm(request.form)
		if form.validate():
			image_file = request.files['file']
			filename = os.path.join(app.config['IMAGES_DIR'],secure_filename(image_file.filename))
			image_file.save(filename)
			flash('Saved %s' % os.path.basename(filename), 'success')
			return redirect(url_for('entries.index'))

	return render_template('entries/image_upload.html', form=form)


@entries.route('/')
def index():
	entries = Entry.query.order_by(Entry.created_timestamp.desc())
	return entry_list('entries/index.html', entries)

@entries.route('/tags/')
def tag_index():
	tags = Tag.query.order_by(Tag.name)
	return object_list('entries/tag_index.html', tags)

@entries.route('/tags/<slug>/')
def tag_detail(slug):
	tag = Tag.query.filter(Tag.slug == slug).first_or_404()
	entries = tag.entries.order_by(Entry.created_timestamp.desc())
	return entry_list('entries/tag_detail.html', entries, tag=tag)


@entries.route('/<slug>/')
def detail(slug):
	entry = get_entry_or_404(slug)
	return render_template('entries/detail.html', entry=entry)

# Flask stores the raw POST data in the special attribute request.form
# WTForms knows how to interpret the raw form data and map it to the fields we defined.
@entries.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
	form = EntryForm()
	if request.method == 'POST':
		form = EntryForm(request.form) # we want to instantiate the EntryForm and pass in the raw form data.
		if form.validate(): # ensure that the form is valid by calling form.validate() .
			# If the form validates, we can finally proceed with saving the entry. To do this, we
			# will call our save_entry helper method, passing in a fresh entry instance
			
			
			# entry = Entry()
			# form.populate_obj(entry)
			# author = g.user -> backref
			entry = form.save_entry(Entry(author=g.user))
			db.session.add(entry)
			db.session.commit()
			flash('Entry "%s" created successfully.' % entry.title, 'success')
			return redirect(url_for('entries.detail', slug=entry.slug))

	return render_template('entries/create.html', form=form)

# The biggest difference is in how we are instantiating the EntryForm . We pass it an
# additional parameter, obj=entry . When WTForms receives an obj parameter, it will
# attempt to pre-populate the form fields with values taken from obj (in this case, our
# blog entry).


@entries.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
	entry = get_entry_or_404(slug, author=g.user)
	if request.method == 'POST':
		# Mengisi atribut dari obj yang dilewatkan dengan data dari kolom form.
		# mengisi object form dengan acuan entry object yang berisi request.form
		form = EntryForm(request.form, obj=entry)
		if form.validate():

			# form.populate_obj(entry) # mengubah data entry object dengan data dari form
			# entry.generate_slug()
			entry = form.save_entry(entry)

			db.session.commit()
			flash('Entry "%s" has been saved.' % entry.title, 'success')
			return redirect(url_for('entries.detail', slug = entry.slug))
	else:
		form = EntryForm(obj = entry)

	return render_template('entries/edit.html', entry=entry, form=form)



@entries.route('/<slug>/delete/', methods=['GET', 'POST'])
@login_required
def delete(slug):
	entry = get_entry_or_404(slug, author = g.user)
	if request.method == 'POST':
		entry.status = Entry.STATUS_DELETED
		db.session.add(entry)
		db.session.commit()
		flash('Entry "%s" has been deleted.' % entry.title, 'success')
		return redirect(url_for('entries.index'))

	return render_template('entries/delete.html', entry=entry)


