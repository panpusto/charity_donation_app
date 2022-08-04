import random

from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
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


class UserRegisterView(View):
    """This function display form to register new user."""
    def get(self, request):
        return render(
            request,
            'register.html',
        )

    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            message = "Hasła nie są identyczne. Proszę wpisz je jeszcze raz."
            return render(request,
                          'register.html',
                          context={
                              'message': message,
                          })

        if name == '' or surname == '' or email == '' or password == '' or password2 == '':
            message = "Pole nie może być puste. Proszę uzupełnij wszystkie dane."
            return render(request,
                          'register.html',
                          context={
                              'message': message,
                          })

        if '@' not in email:
            message = "Adres email jest niepoprawny. Wpisz poprawny adres email."
            return render(request,
                          'register.html',
                          context={
                              'message': message,
                          })

        if User.objects.filter(email=email).exists():
            message = "Konto o tym adresie email już istnieje. Przejdź do strony logowania."
            return render(request,
                          'register.html',
                          context={
                              'message': message,
                          })

        special_symbols = ['!', '@', '#', '%']
        if len(password) < 8 or (not any(char.isdigit() for char in password) or
                                 not any(char.isupper() for char in password) or
                                 not any(char.islower() for char in password) or
                                 not any(char in special_symbols for char in password)):
            message = "Hasło powinno składać się przynajmniej z 8 znaków," \
                      "jednej wielkiej litery, jednej małej litery oraz jednego ze znaków !, @, #, %"
            return render(request,
                          'register.html',
                          context={
                              'message': message,
                          })

        User.objects.create_user(username=email,
                                 first_name=name,
                                 last_name=surname,
                                 email=email,
                                 password=password)

        return redirect('/login')
