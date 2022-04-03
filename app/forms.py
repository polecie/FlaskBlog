from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=4, max=80)])
    remember_me = BooleanField('Remain me')
    submit = SubmitField('Submit')
    #login with social medias

class RegistrationForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    username = StringField(validators=[DataRequired(), Length(min=2, max=15)])
    password = PasswordField(validators=[DataRequired(), Length(min=4, max=80)])
    #confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField()
    submit = SubmitField()
    #register with social medias

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    company = TextAreaField('Company', validators=[Length(min=0, max=140)])
    location = TextAreaField('Location', validators=[Length(min=0, max=140)])
    website = TextAreaField('Website', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')