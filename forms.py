from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, URL, AnyOf, Optional, NumberRange
from wtforms import BooleanField


class AddPetForm(FlaskForm):
    name = StringField('Pet Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired()])
    photo_url = StringField('Photo URL', validators=[URL()])
    age = StringField('Age')
    notes = TextAreaField('Notes')


class EditPetForm(FlaskForm):
    """Form for editing pets"""
    photo_url = StringField('Photo URL', validators=[
                            Optional(), URL(message='Invalid URL')])
    notes = TextAreaField('Notes')
    available = BooleanField('Available')
