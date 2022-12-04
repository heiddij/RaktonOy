from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, EmailField)
from wtforms.validators import InputRequired, Length

class FormContact(FlaskForm):
    name = StringField('Nimi', validators=[InputRequired(), Length(min=5, max=100)])
    phone = StringField('Puhelinnumero', validators=[Length(max=20)])
    email = EmailField('Sähköposti', validators=[InputRequired(), Length(min=5, max=50)])
    message = TextAreaField('Viesti', validators=[Length(max=200)])