from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from charity_app.models import Donation, Institution, Category


class LandingPageView(View):
    """This function display application main page."""
    def get(self, request):
        bags_quantity = Donation.objects.aggregate(Sum('quantity'))
        bags_counter = bags_quantity['quantity__sum']
        institution_counter = Donation.objects.all().count()

        foundations = Institution.objects.filter(type=1).order_by('name')
        paginator_1 = Paginator(foundations, 5)
        foundations_page_number = request.GET.get('page')
        foundations_page_obj = paginator_1.get_page(foundations_page_number)

        non_gov_org = Institution.objects.filter(type=2).order_by('name')
        paginator_2 = Paginator(non_gov_org, 5)
        non_gov_org_page_number = request.GET.get('page')
        non_gov_org_page_obj = paginator_2.get_page(non_gov_org_page_number)

        fundraisers = Institution.objects.filter(type=3).order_by('name')
        paginator_3 = Paginator(fundraisers, 5)
        fundraisers_page_number = request.GET.get('page')
        fundraisers_page_obj = paginator_3.get_page(fundraisers_page_number)

        return render(
            request,
            'index.html',
            context={
                'bags_counter': bags_counter,
                'institution_counter': institution_counter,
                'foundations_page_obj': foundations_page_obj,
                'non_gov_org_page_obj': non_gov_org_page_obj,
                'fundraisers_page_obj': fundraisers_page_obj,
            }
        )


class AddDonationView(LoginRequiredMixin, View):
    login_url = 'login'
    """This function display form to add donation"""
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(
            request,
            'form.html',
            context={
                'categories': categories,
                'institutions': institutions,
            }
        )

    def post(self, request):
        """This function save donation data to database."""
        institution = request.POST['institution']
        categories = request.POST.getlist('categories')
        quantity = request.POST['bags']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        city = request.POST['city']
        zip_code = request.POST['zip_code']
        pick_up_date = request.POST['date']
        pick_up_time = request.POST['time']
        pick_up_comment = request.POST['more_info']
        user = request.user
        organization = Institution.objects.get(pk=institution)

        donation = Donation.objects.create(
            institution=organization,
            quantity=quantity,
            address=address,
            phone_number=phone_number,
            city=city,
            zip_code=zip_code,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=user
        )
        donation.categories.set(categories)
        donation.save()

        return render(request, 'form-confirmation.html')


class DonationConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class UserRegisterView(View):
    """This function display form to register new user."""
    def get(self, request):
        return render(
            request,
            'register.html',
        )

    def post(self, request):
        """
        This function validate input data and create new user account if input data is valid,
        if not it display a message.
        """
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
            return render(
                request,
                'register.html',
                context={
                    'message': message,
                }
            )

        User.objects.create_user(username=email,
                                 first_name=name,
                                 last_name=surname,
                                 email=email,
                                 password=password)

        return redirect('/login')


class LoginView(View):
    """This function display login form."""
    def get(self, request):
        return render(
            request,
            'login.html'
        )

    def post(self, request):
        """
        This function log in authenticated user if username and password
        are correct.
        """
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            return redirect('/')

        if User.objects.filter(email=email).exists():
            message = "Wpisałeś niepoprawne hasło. Spróbuj ponownie lub zresetuj hasło."
            return render(
                request,
                'login.html',
                context={
                    'message': message
                }
            )

        else:
            message = 'Użytkownika nie ma w bazie. Proszę załóż konto.'
            return render(
                request,
                'register.html',
                context={
                    'message': message
                }
            )


class LogoutView(View):
    """This function log out a user"""
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)

        return redirect('/')


class UserProfileView(View):
    def get(self, request):
        """This function display info about user and list of his donations."""
        user_donations = Donation.objects.filter(user_id=request.user.id).order_by('-pick_up_date',
                                                                                   'is_taken',
                                                                                   '-taken_time')
        return render(
            request,
            'user_profile.html',
            context={
                'user_donations': user_donations,
            }
        )


class ArchiveDonationView(View):
    def post(self, request, pk):
        """
        This function allows to confirm that the package has been picked up
        form the user.
        """
        picked_up_donation = request.user.donation_set.get(pk=pk)
        if "picked_up_confirm" in request.POST:
            picked_up_donation.is_taken = True
            picked_up_donation.taken_time = timezone.now()
            picked_up_donation.save()

        return redirect('user-profile')
