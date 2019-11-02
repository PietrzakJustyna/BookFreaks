from django import forms


class LoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

