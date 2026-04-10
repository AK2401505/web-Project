from django import forms
from .models import users
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    
    class Meta:
        model = users
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
        'placeholder': 'Username',
        'class': 'form-control'  
        })
        self.fields['password1'].widget.attrs.update({
        'placeholder': 'Password',
        'class': 'form-control'  
        })
        self.fields['password2'].widget.attrs.update({
        'placeholder': 'Confirm Password',
        'class': 'form-control'  
        })
