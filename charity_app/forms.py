from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from charity_app.validators import password_validate


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Hasło"}),
        validators=[password_validate]
    )
    repeated_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Powtórz hasło"}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "repeated_password"]

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Imię"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Nazwisko"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"})
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeated_password = cleaned_data.get('repeated_password')
        email = cleaned_data.get('email')
        if password != repeated_password:
            msg = "Hasła w obu polach nie są zgodne."
            self.add_error("password", msg)
            self.add_error("repeated_password", msg)

        try:
            if User.objects.get(email=email):
                self.add_error("email", "Konto o podanym adresie email już istnieje.")
        except User.DoesNotExist:
            pass

