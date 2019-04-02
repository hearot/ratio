from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import render
from django.views import generic

from .models import Competition


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
