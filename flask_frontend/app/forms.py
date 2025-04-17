from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional, Email
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one.')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    email = StringField('Email', validators=[Optional()])
    age = IntegerField('Age', validators=[Optional()])
    sex = SelectField('Sex', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    submit = SubmitField('Update Personal Info')

class EditPaymentForm(FlaskForm):
    payment_method = StringField('Credit Card (Mock)', validators=[Optional()])
    submit = SubmitField('Update Payment')

class EditAddressForm(FlaskForm):
    street = StringField('Street', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    province = StringField('Province', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])
    postal_code = StringField('Postal Code', validators=[Optional()])
    submit = SubmitField('Update Address')
