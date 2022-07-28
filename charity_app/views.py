from django.shortcuts import render
from django.views import View


class LandingPageView(View):
    """This function display application main page."""
    def get(self, request):
        return render(
            request,
            'index.html'
        )


class AddDonationView(View):
    """This function display form to add donation"""
    def get(self, request):
        return render(
            request,
            'form.html'
        )


class LoginView(View):
    """This function display login form."""
    def get(self, request):
        return render(
            request,
            'login.html'
        )


class RegisterView(View):
    """This function display register form for new user."""
    def get(self, request):
        return render(
            request,
            'register.html'
        )

