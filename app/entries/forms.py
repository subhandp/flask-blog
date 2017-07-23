import wtforms
from wtforms.validators import DataRequired
from models import Entry, Tag

# list comprehension 
# strip() 	-> menhilangkan karakter dari keseluruhan string (default->whitespace charaters)
# set()		-> list yang immutable dan unik isinya/tidak ada kesamaan
# list()	-> konversi tipe data lain ke list
class TagField(wtforms.StringField):
	# converts the list of Tag instances into a comma-separated list of tag names
	def _value(self):
		if self.data:
			# Display tags as a comma-separated list.
			return ', '.join([tag.name for tag in self.data])
		return ''

	def get_tags_from_string(self, tag_string):
		raw_tags = tag_string.split(',')

		# Filter out any empty tag names.
		tag_names = [name.strip() for name in raw_tags if name.strip()]

		# Query the database and retrieve any tags we have already saved.
		existing_tags = Tag.query.filter(Tag.name.in_(tag_names))

		# Determine which tag names are new.
		new_names = set(tag_names) - set([tag.name for tag in existing_tags])


		# Create a list of unsaved Tag instances for the new tags.
		new_tags = [Tag(name=name) for name in new_names]

		# Return all the existing tags + all the new, unsaved tags.
		return list(existing_tags) + new_tags

	# accepts the comma-separated tag list and converts it into a list of Tag instances
	def process_formdata(self, valuelist):
		if valuelist:
			self.data = self.get_tags_from_string(valuelist[0])
		else:
			self.data = []


class ImageForm(wtforms.Form):
	file = wtforms.FileField('Image file')


# coerce -> memaksa/merubah menjadi int
class EntryForm(wtforms.Form):
	title = wtforms.StringField(
		'Title',
		validators = [DataRequired()])
	body = wtforms.TextAreaField(
		'Body',
		validators = [DataRequired()])
	status = wtforms.SelectField(
		'Entry status',
		choices = (
			(Entry.STATUS_PUBLIC, 'Public'),
			(Entry.STATUS_DRAFT, 'Draft')
		),
		coerce = int)
	tags = TagField(
		'Tags',
		description='Separate multiple tags with commas.')

	# This helper method will populate the entry we pass in with the form data, re-
	# generate the entry's slug based on the title, and then return the entry object
	# MENGISI DATA DARI INSTANCE ENTRY DENGAN RAW DATA WTFORM
	def save_entry(self, entry):
		self.populate_obj(entry) # Mengisi atribut dari obj yang dilewatkan dengan data dari kolom form.
		entry.generate_slug()
		return entry




	# WHY SELF ??
	# Let's say you have a class ClassA which contains a method methodA defined as:

	# def methodA(self, arg1, arg2):
	#     # do something

	# and ObjectA is an instance of this class.

	# Now when ObjectA.methodA(arg1, arg2) is called, python internally converts it for you as:

	# ClassA.methodA(ObjectA, arg1, arg2)

	# The self variable refers to the object itself.
