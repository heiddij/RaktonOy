from flask import Flask, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, form
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import FileUploadField
from wtforms.validators import ValidationError
import imghdr
import os
import os.path as op
from sqlalchemy.event import listens_for
from markupsafe import Markup
from flask_admin.contrib import sqla, rediscli
from flask_migrate import Migrate

# Using SQLAlchemy extension for database
db = SQLAlchemy()

# Create the app
app = Flask(__name__)

app.config.from_object(Config)

# Init the database
db.init_app(app) 

# For db migrations
# When making model modifications use flask db migrate - flask db upgrade
migrate = Migrate(app, db)

# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'static', 'pics')
try:
    os.mkdir(file_path)
except OSError:
    pass

from models import Image, Page

# Delete image
@listens_for(Image, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass

# Custom view for admin to create an image
class ImageView(sqla.ModelView):
    # def _list_thumbnail(view, context, model, name):
    #     if not model.path:
    #         return ''

    #     return Markup('<img src="%s">' % url_for('static',
    #                                              filename=form.thumbgen_filename(model.path)))

    # column_formatters = {
    #     'path': _list_thumbnail
    # }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=file_path)
    }

# Register the admin sites
admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ImageView(Image, db.session))
admin.add_view(ModelView(Page, db.session))
