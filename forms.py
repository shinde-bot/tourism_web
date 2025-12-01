from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf import FlaskForm

# --- Login Form ---
class LoginForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[DataRequired(), Length(min=3, max=80)]
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired(), Length(min=8, max=128)]
    )
    submit = SubmitField('Log In')

# --- Registration Form ---
class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[DataRequired(), Length(min=3, max=80)]
    )
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired(), Length(min=8, max=128)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField('Sign Up')

# --- Forgot Password Form ---
class ForgotPasswordForm(FlaskForm):
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Reset Password')
