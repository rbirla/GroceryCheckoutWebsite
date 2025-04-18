from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional, Email
from app.models import User
from wtforms import RadioField

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
    cardholder_first = StringField('Cardholder Name', validators=[DataRequired(), Length(max=10)])
    cardholder_last = StringField('Last', validators=[DataRequired(), Length(max=10)])
    
    card_number = StringField('Card Number', validators=[DataRequired(), Length(min=15, max=19)])
    expiration_date = StringField('Expiration Date (MM/YY)', validators=[DataRequired(), Length(max=5)])
    cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=3)])
    
    card_type = RadioField('Card Type', choices=[('credit', 'Credit'), ('debit', 'Debit')], validators=[DataRequired()])
    set_primary = BooleanField('Set as primary card')
    
    submit = SubmitField('Add Card')



class EditAddressForm(FlaskForm):
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    province = StringField('Province', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    submit = SubmitField('Update Address')
