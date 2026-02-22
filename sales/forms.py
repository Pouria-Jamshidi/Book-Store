from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from sales.models import Order, StatusChoices

User = get_user_model()


class Increase_user_credit(forms.Form):
    username = forms.ModelChoiceField(queryset=User.objects.all(), required=True, widget=forms.Select(attrs={'class':'form-Select', 'id':'username'}), label='نام کاربری')
    credit = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'form-Control'}), validators=[MinValueValidator(0)], label='مبلغ اضافه شونده به کیف پول')


class PaymentForm(forms.Form):
    use_credit = forms.BooleanField(label='استفاده از شارژ کیف پول',required=False,
                                     widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'id':'use_credit', 'role':'switch'}))
