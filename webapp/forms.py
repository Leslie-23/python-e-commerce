"""
Forms for the e-commerce web application
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, IntegerField, DecimalField, FileField, BooleanField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, EqualTo
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class SignupForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])

class EditProfileForm(FlaskForm):
    """Edit user profile form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])

class ChangePasswordForm(FlaskForm):
    """Change password form"""
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', 
                                   validators=[DataRequired(), EqualTo('new_password')])

class ProductForm(FlaskForm):
    """Add/Edit product form"""
    title = StringField('Product Title', validators=[DataRequired(), Length(min=3, max=255)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    weight = DecimalField('Weight (kg)', validators=[DataRequired(), NumberRange(min=0)])
    product_image = FileField('Product Image', validators=[
        Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])

class CategoryForm(FlaskForm):
    """Add/Edit category form"""
    category_name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=100)])
    parent_category_id = SelectField('Parent Category', coerce=int, validators=[Optional()])

class VariantForm(FlaskForm):
    """Add/Edit variant form"""
    name = StringField('Variant Name', validators=[DataRequired(), Length(min=2, max=100)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    custom_attributes = TextAreaField('Custom Attributes', validators=[Optional()])
    variant_image = FileField('Variant Image', validators=[
        Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])

class SearchForm(FlaskForm):
    """Search form"""
    query = StringField('Search', validators=[DataRequired(), Length(min=1, max=100)])
    category = SelectField('Category', coerce=str, validators=[Optional()])

class CheckoutForm(FlaskForm):
    """Checkout form"""
    delivery_method = SelectField('Delivery Method', 
                                choices=[('standard', 'Standard Delivery'),
                                       ('express', 'Express Delivery')],
                                validators=[DataRequired()])
    payment_method = SelectField('Payment Method',
                               choices=[('credit_card', 'Credit Card'),
                                      ('paypal', 'PayPal'),
                                      ('bank_transfer', 'Bank Transfer')],
                               validators=[DataRequired()])
    delivery_address = TextAreaField('Delivery Address', validators=[DataRequired()])
