from wtforms import Form, StringField, PasswordField, validators, TextAreaField


class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=20)])
    email = StringField('Email', [validators.Email()])
    password = PasswordField('Password', [validators.Length(min=3), validators.EqualTo('password2', 'Passwords must match')])
    password2 = PasswordField('Repeat Password')
    firstname = StringField('Firstname', [validators.Length(min=3, max=20)])
    lastname = StringField('Lastname', [validators.Length(min=3, max=20)])
    about = TextAreaField('About user', [validators.Length(min=10)])

