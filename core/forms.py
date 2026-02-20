from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm
from django.contrib.auth import get_user_model
from .models import App

User = get_user_model()


class PasswordChangeForm(AuthPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.setdefault('class', 'input')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CreateAppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ('name', 'description', 'template')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'My Awesome App',
                'class': 'input',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe what you want to build...',
                'class': 'input',
                'rows': 3,
            }),
            'template': forms.Select(attrs={'class': 'input'}),
        }


class AppEditForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ('name', 'slug', 'description', 'published')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'slug': forms.TextInput(attrs={'class': 'input', 'placeholder': 'my-app'}),
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 3}),
        }

    def clean_slug(self):
        slug = (self.cleaned_data.get('slug') or '').strip().lower()
        if not slug:
            return self.instance.slug or ''
        from django.utils.text import slugify
        slug = slugify(slug) or slug
        if App.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This URL slug is already taken.')
        return slug
