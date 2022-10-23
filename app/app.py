from flask import Flask, url_for, redirect, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, form, AdminIndexView
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
from flask_security import SQLAlchemyUserDatastore, Security, current_user


# Using SQLAlchemy extension for database
db = SQLAlchemy()

# Create the app
app = Flask(__name__)

app.config.from_object(Config)

# Init the database
db.init_app(app) 

# Push the context for working inside the interactive shell
app.app_context().push()

# For db migrations
# When making model modifications use flask db migrate - flask db upgrade
migrate = Migrate(app, db)

# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'static', 'pics')
try:
    os.mkdir(file_path)
except OSError:
    pass

from models import *

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


# Restrict access only for admin role
class AdminMixin():
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


# Custom view for admin to create an image
class ImageView(AdminMixin, sqla.ModelView):
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

    # Restrict access only for admin role

    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=file_path)
    }


class PageView(AdminMixin, ModelView):
    form_choices = {
        'name': [
            ('Etusivu', 'Etusivu'),
            ('Asuntokaupan kuntotarkastus', 'Asuntokaupan kuntotarkastus'),
            ('Väestönsuojan tarkastus', 'Väestönsuojan tarkastus'),
            ('Korjausrakentaminen', 'Korjausrakentaminen'),
            ('Huoneisto- ja toimistoremontit', 'Huoneisto- ja toimistoremontit')
        ]
    }


# Register the admin sites
admin = Admin(app, name='Rakton Oy', template_mode='bootstrap3', index_view=HomeAdminView(name='Home'))
admin.add_view(ImageView(Image, db.session))
admin.add_view(PageView(Page, db.session))


# Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
