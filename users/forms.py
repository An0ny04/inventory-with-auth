from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Products

class UserForm(forms.ModelForm):
    email = forms.EmailField(max_length=200 )
    password = forms.CharField(widget=forms.PasswordInput)
    User._meta.get_field('email')._unique = True

    class Meta:
        model = User
        fields = ('username','email', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('role',)

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price','quantity','status','image']