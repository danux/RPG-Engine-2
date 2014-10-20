# ~*~ coding: utf-8 ~*~
"""
Forms for the auth app.
"""
from django import forms
from django.contrib.auth import get_user_model


class UserCreateForm(forms.ModelForm):
    """
    Registration form responsible for creating users.
    """
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta(object):
        """
        Meta attributes.
        """
        model = get_user_model()
        fields = ['pen_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput
        }

    def clean(self):
        """
        Tests that passwords match and raises an error if they don't.
        :return: {}
        """
        cleaned_data = super(UserCreateForm, self).clean()
        password = cleaned_data.get('password', None)
        password2 = cleaned_data.get('password2', None)
        if password != password2 and (password is not None and password2 is not None):
            # Passwords do not match, raise error
            msg = u'Your passwords did not match.'
            self._errors["password"] = self.error_class([msg])
            self._errors["password2"] = self.error_class([msg])
            del cleaned_data['password']
            del cleaned_data['password2']
        return cleaned_data
