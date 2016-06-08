from wtforms import form, fields, validators
from .models import AdminUser


class LoginForm(form.Form):

    email = fields.TextField(validators=[validators.required(), validators.Email()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_email(self, field):

        user = self.get_user()
        errors = self.errors

        # invalid email address
        if 'email' not in errors and user is None:
            raise validators.ValidationError('Invalid username or password')
        print(errors)
        # no user
        if user is None:
            return

        # check password
        if self.password.data != user.password:
            raise validators.ValidationError('Invalid password!')

    def get_user(self):
        data = self.email.data
        return AdminUser.objects(email=data).first()
