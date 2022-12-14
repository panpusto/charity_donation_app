from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from charity_app.forms import UserCreateForm, ContactForm
from charity_app.models import Donation, Institution, Category
from charity_app.token import account_activation_token


class LandingPageView(View):
    def get(self, request):
        """This function display application main page."""

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
                'contact_form': ContactForm()
            }
        )


class AddDonationView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        """This function display form to add donation"""
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(
            request,
            'form.html',
            context={
                'categories': categories,
                'institutions': institutions,
                'contact_form': ContactForm()
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
        """
        This function display confirmation after successful
        sending donation form.
        """
        return render(request, 'form-confirmation.html')


class UserRegisterView(View):
    def get(self, request):
        """This function display form to register new user."""
        form = UserCreateForm()
        return render(
            request,
            'register.html',
            context={
                'form': form,
                'contact_form': ContactForm()
            }
        )

    def post(self, request):
        """
        This function validate input data and create new user account if input data is valid,
        if not it display a message.
        """
        form = UserCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            user = form.save(commit=False)
            user.set_password(data["password"])
            user.username = data.get("email")
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Oddam w dobre r??ce - aktywacja konta"
            message = render_to_string(
                'account_activation_mail.html',
                {'user': user,
                 'domain': current_site.domain,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': account_activation_token.make_token(user)
                 }
            )
            to_email = data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])

            email.send()

            message_on_site = """
            Na Tw??j adres email zosta?? wys??any link aktywacyjny.
            Aktywuj swoje konto.
            """
            return render(
                request,
                "account_activation_message.html",
                context={
                    'message': message_on_site
                }
            )

        return render(
            request,
            'register.html',
            context={
                "form": form
            }
        )


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            message_on_site = """
            Dzi??kujemy za potwierdzenie adresu email.
            Teraz mo??esz zalogowa?? si?? na swoje konto.
            """
            return render(
                request,
                "account_activation_message.html",
                context={
                    'message': message_on_site
                }
            )

        else:
            message_on_site = "Link aktywacyjny jest niepoprawny."
            return render(
                request,
                "account_activation_message.html",
                context={
                    'message': message_on_site
                }
            )


class LoginView(View):
    """This function display login form."""

    def get(self, request):
        return render(
            request,
            'login.html',
            context={
                'contact_form': ContactForm()
            }
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
            message = "Wpisa??e?? niepoprawne has??o. Spr??buj ponownie lub zresetuj has??o."
            return render(
                request,
                'login.html',
                context={
                    'message': message
                }
            )

        else:
            message = 'U??ytkownika nie ma w bazie. Prosz?? za?????? konto.'
            return render(
                request,
                'login.html',
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
                'contact_form': ContactForm()
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

        if "cancel_picked_up_confirmation" in request.POST:
            picked_up_donation.is_taken = False
            picked_up_donation.taken_time = None
            picked_up_donation.save()

        return redirect('user-profile')


class EditUserProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        """This function display form to editing user profile."""
        return render(
            request,
            'user_edit_profile.html',
            context={
                'contact_form': ContactForm()
            }
        )

    def post(self, request):
        """
        This function save edited user data to database
        if password is valid.
        """
        user = User.objects.get(pk=request.user.id)
        first_name = request.POST['name']
        last_name = request.POST['surname']
        email = request.POST['email']
        valid_password = request.user.check_password(request.POST['password'])

        if valid_password:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            return redirect('user-profile')

        return render(
            request,
            'user_edit_profile.html',
            context={
                'message': "Wprowadzone has??o jest niepoprawne!"
            })


class ChangeUserPasswordView(LoginRequiredMixin, View):
    def get(self, request):
        """This function display for to change user password."""
        return render(
            request,
            'user_change_password.html',
            context={
                'contact_form': ContactForm()
            }
        )

    def post(self, request):
        """
        This function validate last and new user's password
        and save it to database.
        """
        user = User.objects.get(pk=request.user.id)
        old_password = request.user.check_password(request.POST['old_password'])
        new_password = request.POST['new_password']
        new_password_2 = request.POST['repeated_new_password']

        special_symbols = ['!', '@', '#', '%']

        if old_password:
            if len(new_password) < 8 or (not any(char.isdigit() for char in new_password) or
                                         not any(char.isupper() for char in new_password) or
                                         not any(char.islower() for char in new_password) or
                                         not any(char in special_symbols for char in new_password)):
                message = "Has??o powinno sk??ada?? si?? przynajmniej z 8 znak??w," \
                          "jednej wielkiej litery, jednej ma??ej litery oraz jednego ze znak??w !, @, #, %"

                return render(
                    request,
                    'user_change_password.html',
                    context={
                        'message': message
                    }
                )

            if new_password != new_password_2:
                message = "Has??a nie s?? identyczne. Prosz?? wpisz je jeszcze raz."
                return render(request,
                              'user_change_password.html',
                              context={
                                  'message': message,
                              })

            user.set_password(new_password)
            user.save()

            return redirect('login')

        return render(
            request,
            'user_change_password.html',
            context={
                'message': "Wpisane aktualne has??o jest niepoprawne!"
            }
        )


class ContactView(View):
    def post(self, request):
        """This function send user message to website admins."""
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            data = contact_form.cleaned_data

            name = data["name"]
            email = data["email"]
            admins = User.objects.filter(is_staff=True, is_superuser=True)

            send_mail(
                subject=f"Oddam w dobre r??ce - wiadomo???? od {name.title()} / {email}",
                message=data["message"],
                from_email=None,
                recipient_list=[admin.email for admin in admins]
            )

            return render(
                request,
                "contact_message_confirmation.html"
            )

        return redirect('landing-page')
