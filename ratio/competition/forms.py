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

from django import forms
from django.utils.translation import gettext_lazy as _


class GiveAnswer(forms.Form):
    """The form used to give an answer"""

    answer = forms.CharField(label=_('Given answer'), max_length=25)
    """The answer given by the user"""

    question = forms.IntegerField(label=_('Question'))
    """The question the user is answering to"""
