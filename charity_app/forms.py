from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
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


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Imię i nazwisko"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Wiadomość"
            }
        )
    )


class ResetPasswordViaEmail(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("Użytkownika z takim adresem email nie ma w bazie!")
        return email


class NewPasswordConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Hasło"}),
        validators=[password_validate],
        label='Nowe hasło'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Powtórz hasło"}),
        label="Powtórz hasło")

    def clean(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 != password2:
            raise ValidationError("Hasła w obu polach nie są zgodne.")
