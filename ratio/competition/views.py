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

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import generic

from .forms import GiveAnswer
from .models import Answer, Competition, Contestant, User


def api_leaderboard(request, pk: int):
    """Returns a JSON containing all the information
    about the Competition, including points & Contestants."""
    try:
        competition = Competition.objects.get(id=pk)

        return JsonResponse({'ok': True, 'code': 200,
                             'error_message': "",
                             'result': competition.get_leaderboard()})
    except ObjectDoesNotExist:
        return JsonResponse({'ok': False, 'code': 404,
                             'error_message': _("The Competition you want to watch doesn't exist!"),
                             'result': {}})
    except Exception:
        return JsonResponse({'ok': False, 'code': 500,
                             'error_message': _("An error occured."),
                             'result': {}})


def answer(request, pk: int):
    """Returns the Answer questions page and
    validate answers."""
    try:
        competition = Competition.objects.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("The competition you want to play doesn't exist!")})

    if not request.user.is_authenticated:
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("You must be logged in to play a competition!")})

    user = User.objects.get(username=request.user.username)

    try:
        contestant = Contestant.objects.get(competition=competition, user=user)
    except ObjectDoesNotExist:
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("You haven't joined that competition!")})

    if request.method == 'POST':
        form = GiveAnswer(request.POST)

        if not competition.has_started():
            return render(request, "competition/answer.html", {'contestant': contestant,
                                                               'error': True,
                                                               'error_message':
                                                                   _("The competition hasn't begun yet."),
                                                               'form': GiveAnswer})

        if competition.has_ended():
            return render(request, "competition/answer.html", {'contestant': contestant,
                                                               'error': True,
                                                               'error_message':
                                                                   _("The competition is already over."),
                                                               'form': GiveAnswer})

        if form.is_valid():
            try:
                question = competition.get_questions()[form.cleaned_data['question'] - 1]
            except Exception:
                return render(request, "competition/answer.html", {'contestant': contestant,
                                                                   'error': True,
                                                                   'error_message':
                                                                       _("The question number is not valid."),
                                                                   'form': GiveAnswer})

            right = form.cleaned_data['answer'].lower() == question.right_answer.lower()

            if Answer.objects.filter(contestant=contestant, question=question, right=True).exists():
                return render(request, "competition/answer.html", {'contestant': contestant,
                                                                   'error': True,
                                                                   'error_message':
                                                                       _("You've already answered to this question."),
                                                                   'form': GiveAnswer})

            if Answer.objects.filter(contestant=contestant, question=question,
                                     given_answer=form.cleaned_data['answer']).exists():
                return render(request, "competition/answer.html", {'contestant': contestant,
                                                                   'error': True,
                                                                   'error_message':
                                                                       _("You've already given this answer."),
                                                                   'form': GiveAnswer})

            Answer(contestant=contestant, given_answer=form.cleaned_data['answer'],
                   question=question, point=question.point if right else question.wrong,
                   right=right).save()

            if right and (question.point + question.delta) >= question.minimum:
                question.point = question.point + question.delta
                question.save()

            return render(request, "competition/answer.html", {'contestant': contestant, 'form': GiveAnswer,
                                                               'success': _("The answer has been added!")})

    return render(request, "competition/answer.html", {'contestant': contestant, 'form': GiveAnswer})


class CompetitionView(generic.DetailView):
    """Renders the Competition/description page."""
    context_object_name = "competition"
    model = Competition
    template_name = "competition/description.html"


def competitions(request, page: int = 1):
    """Renders the Competitions page."""
    paginator = Paginator(Competition.objects.all().order_by("-start"), 15)

    try:
        races = paginator.get_page(page)
    except EmptyPage:
        races = paginator.get_page(1)

    return render(request, "competition/list.html", {'competitions': races})


def join_competition(request, pk: int):
    """Renders the Join the Competition page."""
    try:
        competition = Competition.objects.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("The competition you want to join doesn't exist!")})

    if not competition.can_join_when_started and competition.has_started():
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("The competition you want to "
                                                                   "join has already begun!")})

    if competition.has_ended():
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("The competition you want to "
                                                                   "join is already over!")})

    if not request.user.is_authenticated:
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("You must be logged in to join a competition!")})

    user = User.objects.get(username=request.user.username)

    if Contestant.objects.filter(competition=competition, user=user).exists():
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("You've already joined this competition!")})

    Contestant(competition=competition, user=user).save()

    return render(request, "competition/join.html", {'competition': competition})


def questions(request, pk: int):
    """Renders the questions page"""
    try:
        competition = Competition.objects.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("The competition you want to watch doesn't exist!")})

    if not competition.has_started():
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("The competition hasn't begun yet.")})

    return render(request, "competition/questions.html", {'competition': competition})


class WatchCompetitionView(generic.DetailView):
    """Renders the Competition leaderboard page."""
    context_object_name = "competition"
    model = Competition
    template_name = "competition/leaderboard.html"

    def get_context_data(self, **kwargs):
        """Gets the other context datas."""
        context = super().get_context_data(**kwargs)

        try:
            context['has_joined'] = context['competition'].is_contestant(
                User.objects.get(username=self.request.user.username))
        except Exception:
            context['has_joined'] = False

        context['questions'] = range(context['competition'].how_many_questions())
        return context
