from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DateField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from app.models import User
from app.retailStore.walmart.api_call import WLMT_STORE_ID_STR, WLMT_PURCH_DATE_STR, WLMT_CARD_TYPE_STR, WLMT_TOTAL_STR, WLMT_LAST_FOUR_STR
import requests
import json

class WalmartReceiptDataForm(FlaskForm):
    cards = [('visa', 'Visa'),('mastercard','Mastercard'),('debit', 'Debit')]

    store_id = IntegerField('Store ID: ')
    purch_date = StringField('Purchase Date: ')
    card_type = SelectField('Card Type: ', choices=cards)
    total = StringField('Total Price: ')
    last_four = IntegerField('Last Four of Credit Card: ')
    submit = SubmitField('Submit')

    def validate_submit(self, submit):
        data = {
            WLMT_STORE_ID_STR : str(self.store_id.data),
            WLMT_PURCH_DATE_STR : str(self.purch_date.data),
            WLMT_CARD_TYPE_STR : str(self.card_type.data),
            WLMT_TOTAL_STR : str(self.total.data),
            WLMT_LAST_FOUR_STR : str(self.last_four.data)
        }

        response = requests.post('https://www.walmart.com/chcwebapp/api/receipts', \
                                json=data)

        if response.status_code != 200:
            raise ValidationError('Receipt not found!')


class AddRecieptToDB(FlaskForm):
    checkbox = BooleanField()
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email("This field requires a valid email address.")])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me: ')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    password2 = PasswordField('Validate Password: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address currently in use.')
