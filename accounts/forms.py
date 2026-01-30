from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

class Register_form(UserCreationForm):
        class Meta:
                model = User
                fields = ['username', 'email', 'password1', 'password2']
                labels = {
                    'username' : 'نام کاربری',
                    'email' : 'ایمیل',
                    'password1' : 'گذرواژه',
                    'password2' : 'تکرار گذرواژه',
                }
                widgets = {
                    'username': forms.TextInput(attrs={'class': 'form-styling field-ltr', 'autofocus': True, 'style':'text-align:left;'}), #autofocus enables curser on this field as the page starts
                    'email': forms.EmailInput(attrs={'class': 'form-styling field-ltr', 'style':'text-align:left;'}),
                }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['password1'].widget.attrs['class'] = 'form-styling field-ltr'
            self.fields['password1'].widget.attrs['style'] = 'text-align:left;'
            self.fields['password2'].widget.attrs['class'] = 'form-styling field-ltr'
            self.fields['password2'].widget.attrs['style'] = 'text-align:left;'

class Login_form(AuthenticationForm):
    username = forms.CharField(
        max_length=20,
        label='نام کاربری',
        widget = forms.TextInput(attrs={'class':'bnazaninBold form-styling field-ltr', 'autofocus': True, 'style':'text-align:left;', 'id':'username'}),#autofocus enables curser on this field as the page starts
    )

    password = forms.CharField(
        label='گذرواژه',
        strip=False, # does not remove the space at the end or begining of user input. passwords should be exact
        widget=forms.PasswordInput(attrs={'class':'bnazaninBold form-styling field-ltr','style':'text-align:left;' , 'id':'password'}),
    )

    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        label="من را بخاطر داشته باش",
        widget=forms.CheckboxInput(attrs={'id':'checkbox'}),
    )