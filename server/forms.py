from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, SelectField, ValidationError
from wtforms.validators import Required, Length, EqualTo, Regexp
from pymongo import MongoClient


class LoginForm(FlaskForm):
    username = StringField('username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
	username = StringField('username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
	user_id = IntegerField('user_id', validators=[Required()])
	password = PasswordField('Password', validators=[Required(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores'), EqualTo('password2', message='you have to confirmed the same password')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	level = SelectField('admin or normal ?', validators=[Required()], choices = [('C', 'normal'), ('B', 'admin')])
	submit = SubmitField('Register')
	
	@staticmethod
	def validate_name(name):
		if MongoClient().safe_protocol.user.find_one({'name':name}):
			return False
		else:
			return True

class RegistrationForm2(FlaskForm):
	username = StringField('username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
	user_id = IntegerField('user_id', validators=[Required()])
	password = PasswordField('Password', validators=[Required(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores'), EqualTo('password2', message='you have to confirmed the same password')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	level = SelectField('admin or normal ?', validators=[Required()], choices = [('C', 'normal')])
	submit = SubmitField('Register')
	
	@staticmethod
	def validate_name(name):
		if MongoClient().safe_protocol.user.find_one({'name':name}):
			return False
		else:
			return True

class ResetForm(FlaskForm):
	new_password = PasswordField('new password', validators=[Required(), EqualTo('new_password2', message='you have to confirmed the same password')])
	new_password2 = PasswordField('Confirm new password', validators=[Required()])
	submit = SubmitField('Reset')