from django import forms
from django.contrib.auth.models import User
from . models import Habit
from django.contrib.auth.forms import AuthenticationForm

class RegisterationForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password =  forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}), required=True)

class HabitCreation(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description']