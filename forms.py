# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# -------------------------------
# Registration Form
# -------------------------------
class RegisterForm(FlaskForm):
    username = StringField(
        "Username", 
        validators=[
            DataRequired(message="Username is required"),
            Length(min=3, max=25, message="Username must be between 3 and 25 characters")
        ]
    )
    email = StringField(
        "Email", 
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Enter a valid email address")
        ]
    )
    password = PasswordField(
        "Password", 
        validators=[
            DataRequired(message="Password is required"),
            Length(min=6, message="Password must be at least 6 characters long")
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password"),
            EqualTo("password", message="Passwords must match")
        ]
    )
    submit = SubmitField("Register")

# -------------------------------
# Login Form
# -------------------------------
class LoginForm(FlaskForm):
    email = StringField(
        "Email", 
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Enter a valid email address")
        ]
    )
    password = PasswordField(
        "Password", 
        validators=[
            DataRequired(message="Password is required")
        ]
    )
    submit = SubmitField("Login")
