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

from typing import Any, Dict

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def send_mail(to: str, template: str, context: Dict[str, Any]):
    """A simple function used to send an email."""

    html_content = render_to_string(f'school/emails/{template}.html', context)
    text_content = render_to_string(f'school/emails/{template}.txt', context)

    msg = EmailMultiAlternatives(context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_activation_email(request, email: str, code: str):
    """A simple function used to send the activation code
    via email."""
    context = {
        'subject': _('Profile activation'),
        'uri': request.build_absolute_uri(reverse('school:activate', kwargs={'code': code})),
    }

    send_mail(email, 'activate_profile', context)


def send_activation_change_email(request, email: str, code: str):
    """A simple function used to send the activation code used to
    change the email via email."""
    context = {
        'subject': _('Change email'),
        'uri': request.build_absolute_uri(reverse('school:change_email_activation', kwargs={'code': code})),
    }

    send_mail(email, 'change_email', context)


def send_reset_password_email(request, email: str, token: str, uid: str):
    """A simple function used to send the activation code used to
    reset the password via email."""
    context = {
        'subject': _('Restore password'),
        'uri': request.build_absolute_uri(
            reverse('school:restore_password_confirm', kwargs={'uidb64': uid, 'token': token})),
    }

    send_mail(email, 'restore_password_email', context)


def send_forgotten_username_email(email: str, username: str):
    """A simple function used to send the forgotten username
    via email."""
    context = {
        'subject': _('Your username'),
        'username': username,
    }

    send_mail(email, 'forgotten_username', context)
