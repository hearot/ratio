from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import generic

from .models import Competition, Contestant, User


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


def join_competition(request, pk: int = 1):
    """Renders the Join the Competition page."""
    try:
        competition = Competition.objects.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("The competition you want to join doesn't exist!")})

    if competition.has_started():
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("The competition you want to "
                                                                   "join has already begun!")})

    if not request.user.is_authenticated:
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("You must be logged in to join a competition!")})

    user = User.objects.get(username=request.user.username)

    if Contestant.objects.filter(competition=competition, user=user).exists():
        return render(request, "layouts/default/page.html", {'error': True,
                                                             'error_message':
                                                                 _("You've already joined this competition!")})

    contestant = Contestant(competition=competition, user=user)
    contestant.save()

    return render(request, "competition/join.html", {'competition': competition})
