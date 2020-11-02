from wtforms import Form, StringField, PasswordField, validators, TextAreaField, ValidationError, SelectField
from blog_pyramid.models import User


def get_user_register_form(postdata, dbsession):
    def validate_username(form, field):
        if dbsession.query(User).filter_by(username=field.data.title()).first():
            raise ValidationError('Username already exists')

    def validate_email(form, field):
        if dbsession.query(User).filter_by(email=field.data.lower()).first():
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


class UserEditForm(Form):
    firstname = StringField('Firstname', [validators.Length(min=3, max=20)])
    lastname = StringField('Lastname', [validators.Length(min=3, max=20)])
    about = TextAreaField('About user', [validators.Length(min=10)])
    role = SelectField("User's role", choices=[('admin', 'admin'), ('editor', 'editor')])


def get_user_email_edit_form(postdata, dbsession):
    def validate_email(form, field):
        if dbsession.query(User).filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already exists')

    class RegisterForm(Form):
        email = StringField('Email', [validators.Email(), validate_email])
    return RegisterForm(postdata)


class LoginForm(Form):
    email = StringField('Email', [validators.Email()])
    password = PasswordField('Password')


class ChangePasswordForm(Form):
    password = PasswordField('Password', [validators.Length(min=3), validators.EqualTo('password2', 'Passwords must match')])
    password2 = PasswordField('Repeat Password')
