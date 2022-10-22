from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import FileUploadField
from wtforms.validators import ValidationError
import imghdr

db = SQLAlchemy()

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app) 

from models import Post

class PostView(ModelView):
    def picture_validation(form, field):
        if field.data:
            filename = field.data.filename.lower()
            if filename[-4:] != '.jpg': 
                raise ValidationError('file must be .jpg')
            if imghdr.what(field.data) != 'jpeg':
                raise ValidationError('file must be a valid jpeg image.')
        field.data = field.data.stream.read()
        return True

    form_columns = ['page', 'photo']
    column_labels = dict(page='Page', photo="Photo")

    def pic_formatter(view, context, model, name):
        return 'NULL' if getattr(model, name) == 'NULL' else 'a picture'

    column_formatters =  dict(photo=pic_formatter)
    form_overrides = dict(photo= FileUploadField)
    form_args = dict(photo=dict(validators=[picture_validation]))

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(PostView(Post, db.session))
