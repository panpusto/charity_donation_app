from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from charity_app.models import Donation


class LandingPageView(View):
    """This function display application main page."""
    def get(self, request):
        bags_quantity = Donation.objects.aggregate(Sum('quantity'))
        bags_counter = bags_quantity['quantity__sum']
        institutions = Donation.objects.aggregate(Sum('institution'))
        institution_counter = institutions['institution__sum']
        return render(
            request,
            'index.html',
            context={
                'bags_counter': bags_counter,
                'institution_counter': institution_counter,
            }
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

