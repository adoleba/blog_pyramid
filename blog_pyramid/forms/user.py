from wtforms import Form, StringField, PasswordField, validators, TextAreaField, ValidationError
from blog_pyramid.models import User


def get_user_form(postdata, dbsession):
    def validate_username(form, field):
        if dbsession.query(User).filter_by(username=field.data).first():
            raise ValidationError('Username already exists')

    def validate_email(form, field):
        if dbsession.query(User).filter_by(email=field.data).first():
            raise ValidationError('Email already exists')

    class RegisterForm(Form):
        username = StringField('Username', [validators.Length(min=3, max=20), validate_username])
        email = StringField('Email', [validators.Email(), validate_email])
        password = PasswordField('Password',
                                 [validators.Length(min=3), validators.EqualTo('password2', 'Passwords must match')])
        password2 = PasswordField('Repeat Password')
        firstname = StringField('Firstname', [validators.Length(min=3, max=20)])
        lastname = StringField('Lastname', [validators.Length(min=3, max=20)])
        about = TextAreaField('About user', [validators.Length(min=10)])
    return RegisterForm(postdata)
