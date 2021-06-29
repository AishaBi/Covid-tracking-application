from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User
from flaskblog import db


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    job_title = StringField('Job Title',
                           validators=[DataRequired(), Length(min=2, max=20)])
    department = StringField('Department',
                           validators=[DataRequired(), Length(min=2, max=20)])
    supervisor = StringField('Supervisor',
                           validators=[DataRequired(), Length(min=2, max=20)])
    manager = StringField('Manager',
                           validators=[DataRequired(), Length(min=2, max=3)])
    high_risk = StringField('High Risk',
                           validators=[DataRequired(), Length(min=2, max=3)])
    health= SelectField('health', choices=[('covid'),('covid-free')])
    h_comment= StringField('Additional Comments',
                           validators=[DataRequired(), Length(min=0, max=60)])
    employment= SelectField('employment', choices=[('working in office'),('part-time in office'), ('working from home')])
    e_comment = StringField('Additional Comments',
                           validators=[DataRequired(), Length(min=0, max=60)])
    date_updated = DateField('Date',format='%m/%d/%Y')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    job_title = StringField('Job Title',
                           validators=[DataRequired(), Length(min=2, max=20)])
    department = StringField('Department',
                           validators=[DataRequired(), Length(min=2, max=20)])
    supervisor = StringField('Supervisor',
                           validators=[DataRequired(), Length(min=2, max=20)])
    manager = StringField('Manager',
                           validators=[DataRequired(), Length(min=2, max=3)])
    high_risk = StringField('High Risk',
                           validators=[DataRequired(), Length(min=2, max=3)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class UpdateHomeForm(FlaskForm):
    health= SelectField('Health Status', choices=[('covid'),('covid-free')])
    h_comment= StringField('Additional Comments',
                           validators=[DataRequired(), Length(min=0, max=60)])
    employment= SelectField('Employment Status', choices=[('working in office'),('part-time in office'), ('working from home')])
    e_comment = StringField('Additional Comments',
                           validators=[DataRequired(), Length(min=0, max=60)])
    submit = SubmitField('Update')

class UpdateMHomeForm(FlaskForm):
    option= SelectField('Please select a page:', choices=[('Analytics'),('Graphs'),('Search')])
    submit = SubmitField ('Enter')

class UpdateGraphForm(FlaskForm):
    option= SelectField('Please select a graph:', choices=[('Line graph'),('Bar chart'),('Pie chart')])
    submit = SubmitField ('Enter')




