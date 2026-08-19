from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Expense, Income

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["title", "amount", "category", "payment_method", "date", "description", "notes"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["title", "amount", "source", "date", "notes"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}

class SignUpForm(UserCreationForm):
    class Meta:
        model = UserCreationForm.Meta.model
        fields = ["username", "password1", "password2"]
