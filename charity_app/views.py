import random
from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from charity_app.models import Donation, Institution


class LandingPageView(View):
    """This function display application main page."""
    def get(self, request):
        bags_quantity = Donation.objects.aggregate(Sum('quantity'))
        bags_counter = bags_quantity['quantity__sum']
        institutions = Donation.objects.aggregate(Sum('institution'))
        institution_counter = institutions['institution__sum']

        foundations = list(Institution.objects.filter(type=1))
        random_foundations = random.sample(foundations, 3)

        non_gov_organisations = list(Institution.objects.filter(type=2))
        random_non_gov_org = random.sample(non_gov_organisations, 4)

        fundraisers = list(Institution.objects.filter(type=3))
        random_fundraisers = random.sample(fundraisers, 2)

        return render(
            request,
            'index.html',
            context={
                'bags_counter': bags_counter,
                'institution_counter': institution_counter,
                'random_foundations': random_foundations,
                'random_non_gov_org': random_non_gov_org,
                'random_fundraisers': random_fundraisers,
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

