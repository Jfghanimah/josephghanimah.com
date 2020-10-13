from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=4, max=40)])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=1, max=100)])    
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=8000)])
