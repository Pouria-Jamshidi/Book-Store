from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

# class Register_form(forms.ModelForm):
#     password = forms.CharField(max_length=20, widget=forms.PasswordInput(), required=True, label="گذرواژه")
#     confirm_password = forms.CharField(max_length=20, widget=forms.PasswordInput(), required=True, label="تکرار گذرواژه")
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'confirm_password']
#
#     def clean(self):
#         data = super().clean()
#         password = data.get('password')
#         confirm_password = data.get('confirm_password')
#
#         validate_password(password)
#         if password and confirm_password and password != confirm_password:
#             raise ValidationError('گذرواژه با تکرار آن مطابقت ندارد.')
#         return data
#
#     def save(self, commit=True):
#         """
#         overriding save method so it hashes our password before saving
#         """
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data.get('password'))
#         user.save()
#         return user

# → due to an error with password , the field was not validated
class Register_form(UserCreationForm):
        class Meta:
                model = User
                fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=40, label='نام کاربری', widget=forms.Textarea(attrs={'class': 'form-control','rows': 1}))
    password = forms.CharField(max_length=40,label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
