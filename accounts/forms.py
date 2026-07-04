from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms

class SignUpForm(UserCreationForm):
  email = forms.EmailField(required=True)

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
