# Ratio: Quisque faber fortunae suae.
# Copyright (C) 2019 Hearot
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import is_safe_url
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView, View, FormView

from .forms import (
    SignInViaUsernameForm, SignInViaEmailForm, SignInViaEmailOrUsernameForm, SignUpForm,
    RestorePasswordForm, RestorePasswordViaEmailOrUsernameForm, RemindUsernameForm,
    ResendActivationCodeForm, ResendActivationCodeViaEmailForm, ChangeProfileForm, ChangeEmailForm,
)
from .models import Activation
from .utils import (
    send_activation_email, send_reset_password_email, send_forgotten_username_email, send_activation_change_email,
)


class GuestOnlyView(View):
    """Redirects to the index page if the user is
    already authenticated"""

    def dispatch(self, request, *args, **kwargs):
        """Checks if the user is authenticated and, if he is,
        it will redirect him to the index page, otherwise it will
        let him log in & do his stuff"""
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class LogInView(GuestOnlyView, FormView):
    """Renders the log in page"""
    template_name = 'school/log_in.html'

    @staticmethod
    def get_form_class(**kwargs):
        """Returns the forms used in the template"""
        if settings.DISABLE_USERNAME or settings.LOGIN_VIA_EMAIL:
            return SignInViaEmailForm

        if settings.LOGIN_VIA_EMAIL_OR_USERNAME:
            return SignInViaEmailOrUsernameForm

        return SignInViaUsernameForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        """Sets a test cookie to make sure the user has
        cookies enabled"""
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Checks if the form is valid"""
        request = self.request

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        if settings.USE_REMEMBER_ME:
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

        login(request, form.user_cache)

        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        url_is_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

        if url_is_safe:
            return redirect(redirect_to)

        return redirect(settings.LOGIN_REDIRECT_URL)


class SignUpView(GuestOnlyView, FormView):
    """Renders the sign up page"""
    template_name = 'school/sign_up.html'
    form_class = SignUpForm

    def form_valid(self, form):
        """Checks if the form is valid and sends the
        activation email"""
        request = self.request
        user = form.save(commit=False)

        if settings.DISABLE_USERNAME:
            user.username = get_random_string()
        else:
            user.username = form.cleaned_data['username']

        if settings.ENABLE_USER_ACTIVATION:
            user.is_active = False

        user.save()

        if settings.DISABLE_USERNAME:
            user.username = f'user_{user.id}'
            user.save()

        if settings.ENABLE_USER_ACTIVATION:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.save()

            send_activation_email(request, user.email, code)

            messages.success(
                request, _('You are signed up. To activate the account, follow the link sent to the mail.'))
        else:
            raw_password = form.cleaned_data['password1']

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            messages.success(request, _('You are successfully signed up!'))

        return redirect('school:index')


class ActivateView(View):
    """Renders the activation page & tries to
    activate the User object"""

    @staticmethod
    def get(request, code):
        """Tries to activate the User object"""
        act = get_object_or_404(Activation, code=code)

        user = act.user
        user.is_active = True
        user.save()

        act.delete()

        messages.success(request, _('You have successfully activated your account!'))

        return redirect('school:log_in')


class ResendActivationCodeView(GuestOnlyView, FormView):
    """Renders the 'resend activation code' page"""
    template_name = 'school/resend_activation_code.html'

    @staticmethod
    def get_form_class(**kwargs):
        """Returns all the forms used that are being
        used to resend the activation code"""
        if settings.DISABLE_USERNAME:
            return ResendActivationCodeViaEmailForm

        return ResendActivationCodeForm

    def form_valid(self, form):
        """Checks if the form is valid"""
        user = form.user_cache

        activation = user.activation_set.first()
        activation.delete()

        code = get_random_string(20)

        act = Activation()
        act.code = code
        act.user = user
        act.save()

        send_activation_email(self.request, user.email, code)

        messages.success(self.request, _('A new activation code has been sent to your email address.'))

        return redirect('school:resend_activation_code')


class RestorePasswordView(GuestOnlyView, FormView):
    """Renders the 'restore password' page and tries to
    restore an user's password"""
    template_name = 'school/restore_password.html'

    @staticmethod
    def get_form_class(**kwargs):
        """Returns all the forms that are being used to
        restore the user's password"""
        if settings.RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME:
            return RestorePasswordViaEmailOrUsernameForm

        return RestorePasswordForm

    def form_valid(self, form):
        """Checks if the form is valid"""
        user = form.user_cache
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()

        send_reset_password_email(self.request, user.email, token, uid)

        return redirect('school:restore_password_done')


class ChangeProfileView(LoginRequiredMixin, FormView):
    """Renders the 'change profile' page and tries to
    change an user's information"""
    template_name = 'school/profile/change_profile.html'
    form_class = ChangeProfileForm

    def get_initial(self):
        """Returns the user's first name &
        last name"""
        user = self.request.user
        initial = super().get_initial()
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        return initial

    def form_valid(self, form):
        """Checks if the form is valid"""
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        messages.success(self.request, _('Profile data has been successfully updated.'))

        return redirect('school:change_profile')


class ChangeEmailView(LoginRequiredMixin, FormView):
    """Renders the 'change email' page and tries to
    change an user's email"""
    template_name = 'school/profile/change_email.html'
    form_class = ChangeEmailForm

    def get_form_kwargs(self):
        """Returns the form keyword arguments by
        adding the user's one"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        """Returns the user's email"""
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        """Checks if the form is valid"""
        user = self.request.user
        email = form.cleaned_data['email']

        if settings.ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.email = email
            act.save()

            send_activation_change_email(self.request, email, code)

            messages.success(self.request, _('To complete the change of email address, click on the link sent to it.'))
        else:
            user.email = email
            user.save()

            messages.success(self.request, _('Email successfully changed.'))

        return redirect('school:change_email')


class ChangeEmailActivateView(View):
    """Renders the 'change email' activation page"""

    @staticmethod
    def get(request, code):
        """Changes the user's email"""
        act = get_object_or_404(Activation, code=code)

        user = act.user
        user.email = act.email
        user.save()

        act.delete()

        messages.success(request, _('You have successfully changed your email!'))

        return redirect('school:change_email')


class RemindUsernameView(GuestOnlyView, FormView):
    """Renders the 'remind username' page"""
    template_name = 'school/remind_username.html'
    form_class = RemindUsernameForm

    def form_valid(self, form):
        """Checks if the form is valid"""
        user = form.user_cache
        send_forgotten_username_email(user.email, user.username)

        messages.success(self.request, _('Your username has been successfully sent to your email.'))

        return redirect('school:remind_username')


class ChangePasswordView(BasePasswordChangeView):
    """Renders the 'change password' page"""
    template_name = 'school/profile/change_password.html'

    def form_valid(self, form):
        """Checks if the form is valid"""
        user = form.save()

        login(self.request, user)

        messages.success(self.request, _('Your password was changed.'))

        return redirect('school:change_password')


class RestorePasswordConfirmView(BasePasswordResetConfirmView):
    """Renders the 'restore password' confirmation page."""
    template_name = 'school/restore_password_confirm.html'

    def form_valid(self, form):
        """Checks if the form is valid"""
        form.save()

        messages.success(self.request, _('Your password has been set. You may go ahead and log in now.'))

        return redirect('school:log_in')


class RestorePasswordDoneView(BasePasswordResetDoneView):
    """Renders the restore password page."""
    template_name = 'school/restore_password_done.html'


class LogOutView(LoginRequiredMixin, BaseLogoutView):
    """Renders the logout page."""
    template_name = 'school/log_out.html'


class IndexView(TemplateView):
    """Renders the default index page."""
    template_name = 'layouts/default/page.html'
