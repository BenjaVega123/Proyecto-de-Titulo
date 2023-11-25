from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from applications.user.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nombre de Usuario',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu Nombre de Usuario'
            },
        )
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '***********'
            }
        )
    )

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            raise ValidationError({
                'username': 'Usuario o contraseña incorrecto.',
                'password': 'Usuario o contraseña incorrecto.',
            })

        return self.cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        return authenticate(username=username, password=password)

class RegisterForm(forms.ModelForm):
    """Form definition for Register."""

    username = forms.CharField(
        label = "Nombre de usuario",
        required = True,
        widget = forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"Crea tu nombre de usuario"
            }
        )
    )
    email = forms.CharField(
        label = "Email",
        required = True,
        widget = forms.EmailInput(
            attrs={
                "class":"form-control",
                "placeholder":"Ingresa tu correo"
            }
        )
    )

    password1 = forms.CharField(
        label = "Contraseña",
        required = True,
        widget = forms.PasswordInput(
            attrs={
                "class":"form-control",
                'placeholder':'Contraseña'
            }
        )
    )
    password2 = forms.CharField(
        label = "Repite contraseña",
        required = True,
        widget = forms.PasswordInput(
            attrs={
                "class":"form-control",
                'placeholder': 'Repite Contraseña'
            }
        )
    )


    class Meta:
        """Meta definition for Registerform."""

        model = User
        fields = ('username','email')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso. Por favor, elige otro.')
        return username

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError(
                'Las contraseñas no coinciden!',
            )
