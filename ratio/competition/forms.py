from django import forms
from django.utils.translation import gettext_lazy as _


class GiveAnswer(forms.Form):
    """The form used to give an answer"""

    answer = forms.CharField(label=_('Given answer'), max_length=25)
    """The answer given by the user"""

    question = forms.IntegerField(label=_('Question'))
    """The question the user is answering to"""
