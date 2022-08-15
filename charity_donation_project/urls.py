"""charity_donation_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from charity_app import views
from django.contrib.auth import views as auth_views

from charity_app.forms import ResetPasswordViaEmail, NewPasswordConfirmForm

urlpatterns = [
    path('admin/', admin.site.urls, name='admin-site'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('', views.LandingPageView.as_view(), name='landing-page'),
    path('add-donation/', views.AddDonationView.as_view(), name='add-donation'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        form_class=ResetPasswordViaEmail), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html",
        form_class=NewPasswordConfirmForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('user-profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('donation-confirmation/', views.DonationConfirmationView.as_view(), name='donation-confirmation'),
    path('add-to-archive/<int:pk>/', views.ArchiveDonationView.as_view(), name='add-to-archive'),
    path('edit-user/', views.EditUserProfileView.as_view(), name='edit-user'),
    path('change-password/', views.ChangeUserPasswordView.as_view(), name='change-password'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    path('send-contact-form/', views.ContactView.as_view(), name='contact-form'),
]
