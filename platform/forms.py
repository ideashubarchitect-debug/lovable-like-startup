from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import App

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CreateAppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'My Awesome App',
                'class': 'input',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe what you want to build... e.g. A todo app with dark mode and drag-and-drop.',
                'class': 'input',
                'rows': 4,
            }),
        }
